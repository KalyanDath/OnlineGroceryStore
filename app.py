import os
from flask import Flask
from flask_security import SQLAlchemySessionUserDatastore , Security
from application import config
from application.config import LocalDevelopmentConfig
from application.models import User, Role
from application.database import db
from flask_restful import Resource, Api
from flask_cors import CORS  #Comment after use

app = None

def create_app():
    app = Flask(__name__)
    CORS(app) ##Comment after use
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    app.logger.info("App setup complete")

    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security = Security(app, user_datastore)
    return app,api

app,api = create_app()

from application.routes import *
from application.api import CategoryAPI, ProductAPI, CategoryProductAPI
api.add_resource(CategoryAPI, "/api/category", "/api/category/<category_id>")
api.add_resource(ProductAPI, "/api/product", "/api/product/<product_id>")
api.add_resource(CategoryProductAPI, "/api/category/<int:category_id>/product")

if __name__ == "__main__":
    app.run(debug=True)
    

