import uuid
from flask import Flask, request
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
        return {"message": "store not found"}, 404


@app.get("/api/items")
def get_items():
    return {"items": list(items.values())}


@app.post("/api/items")
def create_item():
    store_id = request.args.get("store_id")
    if store_id not in stores:
        return {"message": "store not found"}, 404
    item_data = request.get_json()
    item_id = uuid.uuid4().hex
    new_item = {**item_data, "id": item_id, "store_id": store_id}
    items[item_id] = new_item
    return new_item, 201


@app.get("/api/items/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "item not found"}, 404
