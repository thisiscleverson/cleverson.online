from uuid import uuid4
from flask import Blueprint, redirect, session, jsonify, render_template, request

from .models import Contents,Users, db


auth = Blueprint('account', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      USERNAME = request.form.get('username')
      PASSWORD = request.form.get('password')
      
      query = Users.query.filter(Users.username==USERNAME, Users.password==PASSWORD)
      result = query.first()

      if result:
         session["token"] = uuid4()
         return redirect("/")
      else:
         return jsonify({"message": "usuario ou senha incorreta!" })
   return render_template('login.html')


@auth.route('/logout')
def logout():
   session["token"] = None
   return redirect("/")


@auth.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
      #registrar como admin 
      if Users.query.count() == 0:
         db.session.add(
            Users(
               id = str(uuid4()),
               username=request.form.get('username'),
               password=request.form.get('password'),
               userType='admin'
            )
         )
         db.session.commit()
         return redirect("/login")

      else:
         db.session.add(
            Users(
               id = str(uuid4()),
               username=request.form.get('username'),
               password=request.form.get('password'),
               userType='user'
            )
         )
         db.session.commit()
         return redirect("/login")
         
   return render_template('register.html')