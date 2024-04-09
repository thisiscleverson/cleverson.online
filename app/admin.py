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



@admin.route('/editar/<id>', methods=['GET'])
def editor(id):
   if not session.get("token"):
      return redirect('/login')
   
   if request.method == "GET":
      post_data = Contents.query.filter(Contents.id == id).first()

      title  = post_data.title 
      body   = post_data.body
      status = post_data.status
      description = post_data.description
      
      return render_template('admin/editor.html', id=id, title=title, body=body, description=description, is_draft_mode=True, status=status)


@admin.route('/publicar', methods=['GET', 'POST'])
def publish():
   if not session.get("token"):
      return redirect('/login')

   return render_template('admin/editor.html', status=None)