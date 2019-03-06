import os
import json
from flask_restful import Api, Resource, reqparse
import psycopg2
from flask_cors import CORS
from flask import Flask, request
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
    CORS(app, origins="http://localhost:3000", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True, intercept_exceptions=False)
    api = Api(app, catch_all_404s=True)
    return app,conn, api


# testapp, conn = create_app(os.getenv('App_Test'))
app, conn, api = create_app(os.getenv('FLASK_ENV'))



# data = json.load(open('dictionary.data.json'))
# testapi = Api(testapp, catch_all_404s=True)

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

cursor.execute("""CREATE TABLE IF NOT EXISTS articles
           (article_id SERIAL PRIMARY KEY,
           title varchar,
           body varchar);""")


def getarticles():
    cursor.execute("""SELECT * FROM articles;""")
    rows = [x for x in cursor]
    cols = [x[0] for x in cursor.description]
    articles = []
    for row in rows:
      article = {}
      for prop, val in zip(cols, row):
        article[prop] = val
      articles.append(article)
    return articles


def createarticle(title, body):
    try:

        cursor.execute("""SELECT * FROM articles;""")
        cursor.execute("""INSERT INTO articles
                       (title, body)
                       VALUES('{}', '{}');""".format(title, body))
        conn.commit()
        return {'status': 201,
                'message': 'the article was succesfully created'}, 201
    except Exception as e:
        print(e)


class Articles(Resource):
    def get(self):
        return getarticles()

    def post(self):
        args = article_parser.parse_args()
        title = args['title']
        body = args['body']
        return createarticle(title, body)


api.add_resource(Articles, '/articles')
