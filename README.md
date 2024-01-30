# MyBlog

## como rodar esse projeto

* Antes de mais nada, é indicado criar um ambiente virtual.
```sh    
python3 -m venv .venv
```

```sh
export FLASK_app=app
export FLASK_ENV=Development
export FLASK_DEBUG=True

python3 -m flask run -h localhost
```

## migrate 

```sh
flask db init
flask db migrate
flask db update
```