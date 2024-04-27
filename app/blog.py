import uuid
import pytz
from flask import Blueprint, request, redirect, render_template, abort

from .models import Contents, db


blog = Blueprint('blog', __name__)


@blog.route('/', methods=['GET'])
def get_blog():
   contents = Contents.query.filter(Contents.status == "published").order_by(Contents.published_at.desc()).all()

   utc_timezone  = pytz.timezone('UTC')
   user_timezone = pytz.timezone('America/Sao_Paulo')


   for content in contents:
      if content.published_at != None:
         content.published_at = convert_datetime(content.published_at).strftime("%d/%m/%Y, %H:%M %p")

   return render_template('index.html', contents=contents) 


@blog.route('/<slug>', methods=['GET'])
def render_text(slug):
   """ if not session.get("token"):
        return redirect('/login') """

   data = Contents.query.filter(Contents.slug == slug).first()
   
   if data is None:
      abort(404)

   date_published = ""

   if data.published_at != None:
      date_published = convert_datetime(data.published_at).strftime("%d/%m/%Y, %H:%M %p") 

   title = data.title
   body  = data.body
   date  = date_published 
   slug  = data.slug
   description = data.description

   return render_template('blog/render_text.html', title=title, body=body, date=date, slug=slug, description=description)


def convert_datetime(datetime):
   utc_timezone  = pytz.timezone('UTC')
   user_timezone = pytz.timezone('America/Sao_Paulo')

   hour_utc = utc_timezone.localize(datetime)
   return hour_utc.astimezone(user_timezone)


