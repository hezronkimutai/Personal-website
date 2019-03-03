import os
from flask_restful import Api, Resource, reqparse
import psycopg2
from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from instance.config import app_config


def create_app(name_conf):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[name_conf])
    app.config.from_pyfile('config.py')
    app.secret_key = os.getenv('SECRET_KEY')
    db_url = app_config[name_conf].Database_Url
    conn = psycopg2.connect(db_url)
    return app,conn


# testapp, conn = create_app(os.getenv('App_Test'))
app, conn = create_app(os.getenv('FLASK_ENV'))
# testapi = Api(testapp, catch_all_404s=True)
api = Api(app, catch_all_404s=True)
# testjwt = JWTManager(testapp)
jwt = JWTManager(app)
cursor = conn.cursor()

# from app.API.v2.views.articles import *

article_parser = reqparse.RequestParser()
article_parser.add_argument('title',
                            type=str,
                            help='Please provide the title of the article',
                            required=True)
article_parser.add_argument('body',
                            type=str,
                            help='Please provide the body of the article',
                            required=True)


def createarticle(title, body):
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS articles
                   (article_id SERIAL PRIMARY KEY,
                   title varchar,
                   body varchar);""")
        cursor.execute("""SELECT * FROM articles;""")
        cursor.execute("""INSERT INTO articles
                       (title, body)
                       VALUES('{}', '{}');""".format(title, body))
        conn.commit()
        return {'status': 201,
                'message': 'the user was succesfully created'}, 201
    except Exception as e:
        print(e)


class Articles(Resource):
    def post(self):
        args = article_parser.parse_args()
        title = args['title']
        body = args['body']
        return createarticle(title, body)


api.add_resource(Articles, '/articles')
