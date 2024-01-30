from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
<<<<<<< HEAD

db = SQLAlchemy()

def config(app):
=======
=======
>>>>>>> 78d4ede (create auth)
from sqlalchemy import Integer, String, Column, Text, Enum


db = SQLAlchemy()

def config_models(app) -> None:
<<<<<<< HEAD
>>>>>>> 78d4ede (create auth)
=======
>>>>>>> 78d4ede (create auth)
   db.init_app(app)
   app.db = db


class Contents(db.Model):
   __tablename__ = 'contents'

<<<<<<< HEAD
<<<<<<< HEAD
   id    = db.Column(db.String(36), primary_key=True, nullable=True)
   title = db.Column(db.String(256), nullable=True)
   body  = db.Column(db.Text)

   def __init__(self, id: str, title: str, body: int) -> None:
      self.id    = id
      self.title = title
      self.body  = body
=======
=======
>>>>>>> 78d4ede (create auth)
   StatusEnum = Enum('draft', 'published', name='StatusEnum')
   TypeEnum   = Enum('public', 'private', name='TypeEnum')

   id     = Column(String(36), primary_key=True, nullable=False)
   title  = Column(String(256), nullable=False)
   body   = Column(Text)
   status = Column(StatusEnum, default='draft')
   type   = Column(TypeEnum, default='public')


   def __init__(self, id: str, title: str, body:str, status:str, type:str) -> None:
      self.id     = id
      self.title  = title
      self.body   = body 
      self.status = status
      self.type   = type
   

class Users(db.Model):
   __tablename__ = 'users'

   UserTypeEnum   = Enum('user', 'admin', name='TypeEnum')

   id        = Column(String(36), primary_key=True, nullable=False)
   username  = Column(String(20), nullable=False)
   password  = Column(String(100), nullable=False)
   userType = Column(UserTypeEnum, nullable=False, default='user')

   def __init__(self, id:str, username: str, password:str, userType:str) -> None:
      self.id = id
      self.username = username
      self.password = password
<<<<<<< HEAD
      self.userType = userType
>>>>>>> 78d4ede (create auth)
=======
      self.userType = userType
>>>>>>> 78d4ede (create auth)
