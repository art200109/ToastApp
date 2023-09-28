#sall
from flask import Flask, render_template, request, jsonify
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
import urllib.parse.unquote_plus as unquote_plus

client = MongoClient()
client = MongoClient('external-mysql-service.toast.svc', 27017,username=os.environ["mongo_user"],password=os.environ["mongo_password"])

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route("/")
def all_inventory():
    return parse_mongo(client.toast.inventory.find())

@app.route("/",methods=['PUT'])
def update_item():
    data = request.get_json()
    client.toast.inventory.update_one({ "name": data["name"] }, {
        "$set": {"amount":data["amount"]}
    })
    return 'success', 200

@app.route("/<product_name>", methods=['PUT'])
def update_item_amount(product_name):
    product_name = unquote_plus(product_name)

    data = request.get_json()
    product = client.toast.inventory.find_one({ 'name': product_name})

    client.toast.inventory.update_one({ "name": product_name }, {
        "$set": {"amount":product["amount"] + data["delta"]}
    })
    return 'success', 200


@app.route("/<product_name>", methods=['GET'])
def item(product_name):
    product_name = unquote_plus(product_name)
    return parse_mongo(client.toast.inventory.find_one({ 'name': product_name}))

def parse_mongo(data):
    return jsonify(json.loads(json_util.dumps(data)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
