#sallXvvvvvvvvvvvvvfff
from flask import Flask, render_template, request,jsonify
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from bson.objectid import ObjectId
from urllib.parse import unquote_plus

client = MongoClient()
client = MongoClient('external-mysql-service.toast.svc', 27017,username=os.environ["mongo_user"],password=os.environ["mongo_password"])

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
     
@app.route("/")
def all_menu():
    return parse_mongo(client.toast.menu.find())

@app.route("/<product_name>")
def meal(product_name):
    product_name = unquote_plus(product_name)
    return parse_mongo(client.toast.menu.find_one({ 'name': product_name}))

def parse_mongo(data):
    return jsonify(json.loads(json_util.dumps(data)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
