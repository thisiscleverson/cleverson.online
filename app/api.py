import re
from uuid import uuid4
from unidecode import unidecode
from flask import Blueprint, request, redirect, session, render_template, flash, jsonify
from typing import Tuple, Union
from slugify import slugify as slug


from app.models import Contents, db


api = Blueprint('api', __name__ ,url_prefix='/api')


class ContentManager:
   def obtain_draft_title_and_body(self, id: str) -> Tuple[str, str,str] :
      draft_data = Contents.query.filter(Contents.id == id).first()
      title, body, description = draft_data.title, draft_data.body, draft_data.description
      return title, body, description

   def data_valid(self, title: str, content: str) -> bool:
      return len(title.strip()) > 0 and len(content.strip()) > 0

   def update_content(self, id:str, title: str, body: str, description:str, status:str) -> None:
      Contents.query.filter_by(id=id).update({Contents.title:title, Contents.body:body, Contents.status:status, Contents.description:description})
      db.session.commit()
   
   def extract_json_data(self, request:request, keys:list) -> dict:
      """
      Extrai dados JSON da requisição e atribui os valores às variáveis especificadas.

      Args:
         request (flask.request): Objeto de requisição Flask.
         keys (list): Lista de chaves para extrair do JSON.

      Returns:
         dict: Dicionário com os valores extraídos das chaves especificadas.
      """
      data = request.get_json()

      extracted_data = {}
      for key in keys:
         if key in data:
               extracted_data[key] = data[key]
         else:
            return jsonify({
               "error": f"A chave '{key}' está ausente no JSON da requisição.",
               "status_code": 400
            }), 400

      return extracted_data

   def insert_content(self, title: str, body: str, status: str, description:str, accessType: str = 'public') -> None:
      """
      status: "published" or "draft"
      accessType: "public" or "private"
      """
      db.session.add(
         Contents(
            id=str(uuid4()),
            title=title,
            body=body,
            slug=slug(title),
            status=status,
            accessType=accessType,
            description=description
         )
      )
      db.session.commit()



@api.route('/publish',methods=['POST'])
def publish_post():
   if not session.get("token"):
      return jsonify({
         "error": "acesso não autorizado.",
         "status_code":401
      }), 401
   
   if request.method != "POST":
      return jsonify({
         "error": "Método não permitido", 
         "message": "Somente o método post é permitido para este terminal.",
         "status_code": 405
      }), 405

   contentManager = ContentManager()
   expected_keys = ['title', 'body', 'description', 'status_publication']

   data = contentManager.extract_json_data(request, expected_keys)
   if isinstance(data, tuple):  
      return data

   title              = data['title']
   body               = data['body']
   description        = data['description']
   status_publication = data['status_publication']

   if not contentManager.data_valid(title, body):
      return jsonify({
         "message": "O titulo ou texto não está preenchido adequadamente! Por favor, verifique se você preencheu os campo corretamente!",
         "status_code": 400
      }), 400

   contentManager.insert_content(
      title=title,
      body=body,
      status=status_publication,
      description=description
   )

   return jsonify({
      "message": "publicação feita com sucesso.",
      "status_code": 200
   }), 200


@api.route('/delete/post/<id>', methods=['DELETE'])
def delete_post(id):
   if not session.get("token"):
      return jsonify({
         "error": "acesso não autorizado.",
         "status_code":401
      }), 401
    
   Contents.query.filter(Contents.id == id).delete()
   db.session.commit()

   return jsonify({
      "message":"o post foi deletado com sucesso.",
      "status_code":200
   }), 200


@api.route('/update/<id>', methods=['PUT'])
def update_post(id):
   if not session.get("token"):
      return jsonify({
         "error": "acesso não autorizado.",
         "status_code":401
      }), 401

   if request.method != "PUT":
      
      return jsonify({
         "error": "Método não permitido", 
         "message": "Somente o método post é permitido para este terminal.",
         "status_code": 405
      }), 405

   contentManager = ContentManager()
   
   expected_keys = ['title', 'body', 'description', 'status_publication']

   data = contentManager.extract_json_data(request, expected_keys)
   if isinstance(data, tuple):  
      return data
   
   title              = data['title']
   body               = data['body']
   description        = data['description']
   status_publication = data['status_publication']

   if not contentManager.data_valid(title, body):
      return jsonify({
         "message": "O titulo ou texto não está preenchido adequadamente! Por favor, verifique se você preencheu os campo corretamente!",
         "status_code": 400
      }), 400
   
   contentManager.update_content(
      id=id,
      title=title,
      body=body,
      status=status_publication,
      description=description
   )

   return jsonify({
      "message": f'o {title} foi atualizado com sucesso.',
      "status_code": 200
   }), 200
      
   
   

