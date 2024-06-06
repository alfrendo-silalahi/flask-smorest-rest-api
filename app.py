import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores

app = Flask(__name__)


@app.get("/api/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/api/stores")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id": store_id}
    stores[store_id] = new_store
    return new_store, 201


@app.get("/api/stores/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="store not found")


@app.get("/api/items")
def get_items():
    return {"items": list(items.values())}


@app.post("/api/items")
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


@app.get("/api/items/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="item not found")
