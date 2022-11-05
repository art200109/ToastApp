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
     
@app.route("/<product_id>", methods=['POST'])
def order(product_id):
    username  = request.args.get('username', None)
    client.toast.orders.insert_one({ "product_id":product_id, "username": username })
    return 'success', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
