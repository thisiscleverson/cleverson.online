FROM python:3.11

WORKDIR /var/www/cleverson.online

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . . 

CMD ['gunicorn','-b', '0.0.0.0:5000', 'wsgi:app']
