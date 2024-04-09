import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_session import Session

from .models import config_models
from .errorhandler import page_not_found, internal_error


db_dir = '/.database'


def config_database_path(db_dir):
   path_dir = os.path.expanduser('~') + db_dir
   os.makedirs(path_dir, exist_ok=True)
   return os.path.join(path_dir, 'blog.db')


def create_register_blueprint(app):
   from .auth import auth
   from .admin import admin
   from .blog import blog
   from .api import api
   
   app.register_blueprint(auth)
   app.register_blueprint(admin)
   app.register_blueprint(blog)
   app.register_blueprint(api)


def create_register_erro_handler(app):
   app.register_error_handler(404, page_not_found)
   app.register_error_handler(500, internal_error)


def create_app():
   app = Flask(
      __name__,
      template_folder='../templates',
      static_folder='../static'
   )

   app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{config_database_path(db_dir)}' 
   app.config["SESSION_PERMANENT"] = False
   app.config["SESSION_TYPE"] = "filesystem"

   Session(app)
   config_models(app) 
   Migrate(app, app.db)
   create_register_blueprint(app)
   create_register_erro_handler(app)

   return app


