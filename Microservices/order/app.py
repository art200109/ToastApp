#sall
from flask import Flask, render_template, request
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from datetime import datetime

client = MongoClient()
client = MongoClient('external-mysql-service.toast.svc', 27017)

menu_url = "http://menu.toast.svc:8080"

app = Flask(__name__)
     
@app.route("/", methods=['POST'])
def order():
    data = request.get_json()
    data["order_time"] = datetime.today()
    client.toast.orders.insert_one(data)
    
    with urllib.request.urlopen(menu_url+"/"+data["product_id"]) as url:
            meal = json.load(url)
    return 'success', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
