#sall
from flask import Flask, render_template, request
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

client = MongoClient()
client = MongoClient('external-mysql-service.toast.svc', 27017)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route("/")
def all_inventory():
    return parse_mongo(client.toast.inventory.find())

@app.route("/",methods=['PUT'])
def update_item():
    data = request.get_json()
    client.toast.inventory.update_one({ "name": data["name"] }, {
        "$set": {"amount":data["amount"], "confirmed":data["confirmed"]}
    })
    return 'success', 200


@app.route("/<product_name>")
def item(product_name):
    return parse_mongo(client.toast.inventory.find_one({ 'name': product_name}))

def parse_mongo(data):
    return json.loads(json_util.dumps(data))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
