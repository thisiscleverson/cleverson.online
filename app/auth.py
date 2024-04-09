import bcrypt
from uuid import uuid4
from flask import Blueprint, redirect, session, render_template, request, flash
from sqlalchemy.sql import exists
from typing import Tuple

from app.models import Users, db

auth = Blueprint('auth', __name__)


class Auth:
   def get_hash_password(self, username:str) -> str:
      hash_password = Users.query.filter_by(username=username).first().password
      return hash_password


   def get_user_type(self,username:str) -> str:
      user_type = Users.query.filter_by(username=username).first().userType
      return user_type


   def check_username_exist(self, username:str) -> bool:
      return Users.query.filter(Users.username == username).first()


   def get_username_and_password(self) -> Tuple[str,str]:
      return request.form.get('username'), request.form.get('password')


   def register_user(self, username:str, password:str, user_type:str) -> None:
      db.session.add(
         Users(
               id=str(uuid4()),
               username=username,
               password=self.encrypt_password(password),
               userType=user_type
         )
      )
      db.session.commit()


   def encrypt_password(self, password:str) -> str:
      byte_password = password.encode('utf-8')
      hash_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
      return hash_password



@auth.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      auth = Auth()

      username, password = auth.get_username_and_password()

      if not auth.check_username_exist(username):
         flash("Usuário não existe!")
         return redirect("/login") 

      hashpass  = auth.get_hash_password(username)
      user_type = auth.get_user_type(username)

      if not bcrypt.checkpw(password.encode('utf-8'), hashpass):
         flash("Usuário ou senha incorretas!")
         return redirect("/login") 
      
      if user_type != 'admin':
         flash("Você não tem permissão para acessar essa página!\nÉ necessário pedir permissão para o administrador da página!")
         return redirect("/login") 

      session["token"] = uuid4()
      return redirect("/admin")  

   return render_template('auth/login.html')


@auth.route('/logout')
def logout():
   session["token"] = None
   return redirect("/")


@auth.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      auth = Auth()

      username, password = auth.get_username_and_password()

      # registrar como admin
      if Users.query.count() == 0:
         auth.register_user(
            username=username,
            password=password,
            user_type='admin'
         )
         return redirect("/login")

      elif not auth.check_username_exist(username):
         auth.register_user(
            username=username,
            password=password,
            user_type='user'
         )
         return redirect("/login")
      
      flash("Usuário já cadastrado!")

   return render_template('auth/register.html')

