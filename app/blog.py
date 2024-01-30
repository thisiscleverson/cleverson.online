<<<<<<< HEAD
<<<<<<< HEAD
from flask import Blueprint, abort, jsonify, request
from .models import Contents, db
import uuid

bp_blog = Blueprint('blog',__name__, subdomain='blog')


@bp_blog.route('/', methods=['GET'])
def list_blog():
   contents = Contents.query.all()
   
   response = []
   for data in contents:
      response.append({
         "id": data.id,
         "title" : data.title,
         "body": data.body
      })
   return jsonify(response), 200


@bp_blog.route('/post', methods=['POST'])
def post():
   data = request.get_json()

   query = Contents(
      id    = str(uuid.uuid4()),
      title = data['title'],
      body  = data['body']
   )

   db.session.add(query)

   try:
      db.session.commit()
   except Exception as error:
      print(error)
      return "Error!", 400

   return "Data entered successfully!", 201
=======
=======
>>>>>>> 78d4ede (create auth)
import uuid
from flask import Blueprint, request, redirect, session

from .models import Contents, db


blog = Blueprint('blog', __name__)


@blog.route('/', methods=['GET'])
def get_blog():
   if not session.get("token"):
      return redirect('/login')
<<<<<<< HEAD
   return "HELLO world!"
>>>>>>> 78d4ede (create auth)
=======
   return "HELLO world!"
>>>>>>> 78d4ede (create auth)
