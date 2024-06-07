import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores, items

blueprint = Blueprint(
    "items", __name__, url_prefix="/api/items", description="operation on items"
)


@blueprint.get("")
def get_items():
    return {"items": list(items.values())}


@blueprint.post("")
def create_item():
    store_id = request.args.get("store_id")
    item_data = request.get_json()
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            404,
            message="bad request :: ensure 'price' and 'name' are included in the json payload",
        )

    if store_id not in stores:
        abort(404, message="store not found")
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id, "store_id": store_id}
    items[item_id] = new_item
    return new_item, 201


@blueprint.get("/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="item not found")


@blueprint.put("/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message="item not found")


@blueprint.delete("/<string:item_id>")
def delete_store(item_id):
    try:
        del items[item_id]
        return {"message": "item deleted"}
    except:
        abort(404, message="item not found")
