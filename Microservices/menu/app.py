#sall
from flask import Flask, render_template, request
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

client = MongoClient()
client = MongoClient('external-mysql-service.myproject.svc', 10974)

app = Flask(__name__)
     
@app.route("/menu")
def menu():
    return json.loads(json_util.dumps(client.toast.menu.find()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
