from flask import Flask
from os import path

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'eyfewfknpoajsdfouaefp'
    #app.config.from_pyfile(path.join("..", "PROPERTIES"), silent=False)
    #myversion = app.config.get("VERSION")

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app

