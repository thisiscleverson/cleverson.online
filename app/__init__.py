import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_session import Session

from .models import config_models

db_dir = '/.database'


def config_database_path(db_dir):
   path_dir = os.path.expanduser('~') + db_dir
   os.makedirs(path_dir, exist_ok=True)
   return os.path.join(path_dir, 'blog.db')


def create_register_blueprint(app):
   from .auth import auth
   from .admin import admin
   from .blog import blog

   app.register_blueprint(auth)
   app.register_blueprint(admin)
   app.register_blueprint(blog)


def erro_handler(app):
   @app.errorhandler(404)
   def page_not_found(error):
      return render_template('errorHandler/404.html'), 404

   @app.errorhandler(500)
   def internal_error(error):
      return render_template('errorHandler/500.html'), 500


def create_app():
   app = Flask(__name__,
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

   erro_handler(app)

   return app


