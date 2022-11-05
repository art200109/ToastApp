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
     
@app.route("/")
def all_inventory():
    return json_util.dumps(client.toast.inventory.find())

@app.route("/<product_name>")
def item(product_name):
    return json_util.dumps(client.toast.inventory.find_one({ 'name': product_name}))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
