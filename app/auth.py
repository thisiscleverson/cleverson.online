import bcrypt
from uuid import uuid4
from flask import Blueprint, redirect, session, render_template, request, flash
from sqlalchemy.sql import exists

from app.models import Users, db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username, password = get_username_and_password()

        if check_username_exist(username):

            hashpass = get_hash_password(username)
            user_type = get_user_type(username)

            if bcrypt.checkpw(password.encode('utf-8'), hashpass):
                if user_type == 'admin':
                    session["token"] = uuid4()
                    return redirect("/admin")
                else:
                    flash("Você não tem permissão para acessar essa página!\nÉ necessário pedir permissão para o admin da página!")
            else:
                flash("Usuário ou senha incorretas!")
        else:
            flash("Usuário não existe!")
    return render_template('auth/login.html', error=error)


@auth.route('/logout')
def logout():
    session["token"] = None
    print('logout')
    return redirect("/admin")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username, password = get_username_and_password()

        # registrar como admin
        if Users.query.count() == 0:
            register_user(
                username=username,
                password=password,
                user_type='admin'
            )
            return redirect("/login")
        else:
            username_exist = check_username_exist(username)
            if not username_exist:
                register_user(
                    username=username,
                    password=password,
                    user_type='user'
                )
                return redirect("/login")
            else:
                error = "usuário já cadastrado!"
    return render_template('auth/register.html', error=error)



def get_hash_password(username):
    hash_password = Users.query.filter_by(username=username).first().password
    return hash_password


def get_user_type(username):
    user_type = Users.query.filter_by(username=username).first().userType
    return user_type


def check_username_exist(username):
    query = Users.query.filter(Users.username == username)
    result = query.first()
    return result


def get_username_and_password():
    return request.form.get('username'), request.form.get('password')


def register_user(username, password, user_type):
    db.session.add(
        Users(
            id=str(uuid4()),
            username=username,
            password=encrypt_password(password),
            userType=user_type
        )
    )
    db.session.commit()


def encrypt_password(password):
    byte_password = password.encode('utf-8')
    hash_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
    return hash_password
