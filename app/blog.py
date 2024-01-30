import uuid
from flask import Blueprint, request, redirect, render_template, abort

from .models import Contents, db


blog = Blueprint('blog', __name__)


@blog.route('/', methods=['GET'])
def get_blog():
   contents = Contents.query.filter(Contents.status == "published").order_by(Contents.created_at.desc()).all()
   return render_template('index.html', contents=contents) 


@blog.route('/<slug>', methods=['GET'])
def render_text(slug):
   """ if not session.get("token"):
        return redirect('/login') """

   data = Contents.query.filter(Contents.slug == slug).first()
   
   if data is None:
      abort(404)

   title = data.title
   body  = data.body
   date  = data.created_at.strftime("%d/%m/%Y, %H:%M %p") 

   return render_template('blog/render_text.html', title=title, body=body, date=date)

