import re
from unidecode import unidecode
from uuid import uuid4
from flask import Blueprint, request, redirect, session, render_template, flash, jsonify
from app.models import Contents, db

admin = Blueprint('admin', __name__)

@admin.route('/admin', methods=['GET'])
def home():
    if not session.get("token"):
        return redirect('/login')

    draft_list    = Contents.query.filter(Contents.status == "draft").all()
    contents_list = Contents.query.filter(Contents.status == "published").all()

    return render_template('admin/home.html', draft_list=draft_list, contents_list=contents_list)


@admin.route('/publish', methods=['GET', 'POST'])
def publish():
    if not session.get("token"):
        return redirect('/login')

    if request.method == "POST":
        title, content, description  = get_title_content_description()

        if data_valid(title, content):
            insert_content(
                title=title,
                body=content,
                status='published',
                accessType='public',
                description=description
            )
            return redirect('/')

        flash("O titulo ou texto não está preenchido adequadamente! Por favor, verifique se você preencheu os campo corretamente!")

    return render_template('admin/editor.html', is_draft_mode=True)


@admin.route('/update/<id>', methods=['GET', 'POST', 'PUT'])
def update(id):
    if not session.get("token"):
        return redirect('/login')

    if request.method == "POST":
      data = request.get_json()

      title = data['title']
      body  = data['body']
      description = data['description']

      if data_valid(title, body):
        update_content(id=id, title=title,body=body, description=description)
        return jsonify({"status_code": 200, 'success': True}), 200
      
      return jsonify({"status_code":200, "success":True, "message":"O titulo ou texto não está preenchido adequadamente! Por favor, verifique se você preencheu os campo corretamente!"}), 200

    if request.method == 'PUT':
        data = request.get_json()

        title = data['title']
        body  = data['body']
        description = data['description']

        if data_valid(title, body):
            update_content(id=id, title=title,body=body, status='published', description=description)
            return jsonify({"status_code": 200, 'success': True}), 200

    if request.method == "GET":
        title, body, description = obtain_draft_title_and_body(id)
        return render_template('admin/editor.html', id=id, title=title, body=body, description=description, is_draft_mode=False)


@admin.route('/draft', methods=['POST'])
def draft():
    if request.method == "POST":
        data = request.get_json()

        title = data['title']
        content = data['body']
        description = data['description']

        if data_valid(title, content):
            insert_content(
                title=title,
                body=content,
                status='draft',
                accessType='public',
                description=description
            )
            return jsonify({"status_code": 200, 'success': True}), 200

        return jsonify({
            "error": {
                "status_code": 400,
                "message": "Os campos título e texto não foram preenchidos adequadamente. Por favor, verifique se você preencheu os campos corretamente."
            }
        }), 400

    return jsonify({"status_code": 400, "erro": "Método não permitido"}), 405


@admin.route('/delete/post/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    if not session.get("token"):
        return jsonify({
            "status": "error",
            "message": "Você não tem permissão para deletar este post.",
            "code": 403
        }), 403
    
    Contents.query.filter(Contents.id == post_id).delete()
    db.session.commit()

    return jsonify({"status_code":200, "success":True}), 200

def obtain_draft_title_and_body(id: str):
    query = Contents.query.filter(Contents.id == id)
    draft_data = query.first()
    title, body, description = draft_data.title, draft_data.body, draft_data.description
    return title, body, description

def get_title_content_description():
    return request.form.get("title"), request.form.get("markdown-content"), request.form.get('description')

def data_valid(title: str, content: str) -> bool:
    return len(title.strip()) > 0 and len(content.strip()) > 0

def update_content(id:str, title: str, body: str,description:str, status:str = None) -> None:
   if status is None:
      Contents.query.filter_by(id=id).update({Contents.title:title, Contents.body:body, Contents.description:description})
      db.session.commit()
      return
   Contents.query.filter_by(id=id).update({Contents.title:title, Contents.body:body, Contents.status:status, Contents.description:description})
   db.session.commit()

def generate_slug(title:str) -> str:
   title = unidecode(title)
   slug  = re.sub(r'[^\w\s-]', '', title.lower())
   slug  = re.sub(r'\s', '-', slug)
   return slug

def insert_content(title: str, body: str, status: str, accessType: str, description:str) -> None:
   """
   status: "published" or "draft"
   accessType: "public" or "private"
   """
   db.session.add(
      Contents(
         id=str(uuid4()),
         title=title,
         body=body,
         slug=generate_slug(title),
         status=status,
         accessType=accessType,
         description=description
      )
   )
   db.session.commit()
