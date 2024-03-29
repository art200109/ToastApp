#sall
from flask import Flask, render_template, request, jsonify
import os
import urllib.request, json 
from pymongo import MongoClient
from bson import json_util, ObjectId
import json
from datetime import datetime
import requests
from urllib.parse import quote_plus

client = MongoClient()
client = MongoClient('external-mysql-service.toast.svc', 27017,username=os.environ["mongo_user"],password=os.environ["mongo_password"])

menu_url = "http://menu.toast.svc:8080"
inventory_url = "http://inventory.toast.svc:8080"


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True 

@app.route("/", methods=['GET'])
def all_orders():
    return parse_mongo(client.toast.orders.find())

@app.route("/", methods=['POST'])
def order():
    data = request.get_json()
    data["order_time"] = datetime.today()
    client.toast.orders.insert_one(data)
    
    with urllib.request.urlopen(menu_url+"/"+quote_plus(data["product_name"])) as url:
            meal = json.load(url)
            
    with urllib.request.urlopen(inventory_url) as url:
        inventory = json.load(url)
        
    for key in meal['recipe']:
        def filter_by_name(item):
            return item["name"] == key
        inventory_item = list(filter(filter_by_name, inventory))[0]
        inventory_item['amount'] = int(inventory_item['amount']) - int(meal['recipe'][key])
        if(inventory_item['amount'] < 0):
            return 'not enough', 422
        response = requests.put(inventory_url, json=inventory_item)
        response.raise_for_status()
    
    return 'success', 200

def parse_mongo(data):
    return jsonify(json.loads(json_util.dumps(data)))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
