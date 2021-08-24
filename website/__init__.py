from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from os import path

app = Flask(__name__)
db = SQLAlchemy()
ma = Marshmallow()
UPLOAD_FOLDER = '/Users/lucasrahn/batcave/extra_scripts/allure-report-server'
DB_NAME = 'database.db'

@app.before_request
def clear_trailing():
    from flask import redirect, request

    rp = request.path 
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

def create_app():

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = 'this_is_my_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['JSON_SORT_KEYS'] = False
    app.url_map.strict_slashes = False
    db.init_app(app)

    from .views import views
    from .api import api
    app.register_blueprint(views)
    app.register_blueprint(api, url_prefix='/api')

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
