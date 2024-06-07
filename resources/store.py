import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blueprint = Blueprint(
    "stores", __name__, url_prefix="/api/stores", description="operation on stores"
)


@blueprint.get("")
def get_stores():
    return {"stores": list(stores.values())}


@blueprint.post("")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@blueprint.get("/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="store not found")


@blueprint.delete("/<string:store_id>")
def delete(store_id):
    try:
        del stores[store_id]
        return {"message", "store deleted"}
    except KeyError:
        abort(404, message="store not found")
