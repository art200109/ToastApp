#sallX
from flask import Flask, render_template, request,jsonify
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from bson.objectid import ObjectId

client = MongoClient()
client = MongoClient('external-mysql-service.toast.svc', 27017)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
     
@app.route("/")
def all_menu():
    return parse_mongo(client.toast.menu.find())

@app.route("/<product_id>")
def meal(product_id):
    return parse_mongo(client.toast.menu.find_one(ObjectId(product_id)))

def parse_mongo(data):
    return jsonify(json.loads(json_util.dumps(data)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
