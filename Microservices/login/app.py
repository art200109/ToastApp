#sall
from flask import Flask, render_template, request
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json

client = MongoClient()
client = MongoClient('external-mysql-service.myproject.svc', 27017)

app = Flask(__name__)
     
@app.route("/login/<user_name>")
def login(user_name):
    return json_util.dumps(client.toast.users.find_one({"user_name": user_name}))
    #return json.loads(json_util.dumps(client.toast.menu.find()))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)