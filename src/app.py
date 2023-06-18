from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name":"intial store",
        "items": [
            {
                "name": "Chair",
                "price": "19,99"
            }
        ]
    }
]


# http://127.0.0.1:5000/store

# zeige mir alle stores und die dazugehörigen items
@app.get("/store")
def get_stores():
    return {"stores": stores}

# neuen Store hinzufügen
@app.post("/store")
def create_store():
    new_store = request.get_json()
    stores.append(new_store)
    return new_store, 201

# Item in einem der existierenden Stores erstellen
# <string:name> ist ein parameter der in der URL
# hier kann man bspw. den Namen eines Stores eingeben 
@app.post("/store/<string:name>/item")
def create_item(name):
    new_item = request.get_json()
    print(type(new_item))
    for store in stores:
        if store["name"] == name:
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if name == store["name"]:
            return {"name": store["name"]}
    return {"message":"Store not found"}, 404


@app.get("/store/<string:name>/items")
def get_items(name):
    for store in stores:
        if name == store["name"]:
            return {"items": store["items"]}, 200
    return {"message":"Store not found"}, 404