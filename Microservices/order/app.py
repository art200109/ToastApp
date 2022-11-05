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
     
@app.route("/", methods=['POST'])
def order():
    client.toast.orders.insert_one(request.args.to_dict())
    return 'success', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
