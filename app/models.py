from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, Text, Enum, CheckConstraint, DateTime


db = SQLAlchemy()

def config_models(app) -> None:
   db.init_app(app)
   app.db = db


class Contents(db.Model):
   __tablename__ = 'contents'

   id          = Column(String(36), primary_key=True, nullable=False, unique=True)
   title       = Column(String(256), nullable=False)
   body        = Column(Text)
   slug        = Column(String(256), nullable=False, unique=True)
   status      = Column(String, CheckConstraint("status IN ('published', 'draft')"), default='draft')
   accessType  = Column(String, CheckConstraint("type IN ('public', 'private')"), default='public')
   description = Column(String(1000), default='') 
   created_at  = Column(DateTime, default=datetime.utcnow)
   updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


   def __init__(self, id: str, title: str, body:str, slug:str, status:str, accessType:str, description:str) -> None:
      self.id          = id
      self.title       = title
      self.body        = body
      self.slug        = slug
      self.status      = status
      self.accessType  = accessType
      self.description = description
   

class Users(db.Model):
   __tablename__ = 'users'

   id         = Column(String(36), primary_key=True, nullable=False, unique=True)
   username   = Column(String(50), nullable=False, unique=True)
   password   = Column(String(100), nullable=False)
   userType   = Column(String, CheckConstraint("userType IN ('admin' , 'user')"), nullable=False, default='user')
   created_at = db.Column(db.DateTime, default=datetime.utcnow)
   updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

   def __init__(self, id:str, username: str, password:str, userType:str) -> None:
      self.id = id
      self.username = username
      self.password = password
      self.userType = userType