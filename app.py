import uuid
from flask import Flask, request
from flask_smorest import abort, Api
from db import items, stores
from resources.item import blueprint as ImportBlueprint
from resources.store import blueprint as StoreBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Goods Store API"
app.config["API_VERSION"] = "v1.0.0"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

api.register_blueprint(ImportBlueprint)
api.register_blueprint(StoreBlueprint)
