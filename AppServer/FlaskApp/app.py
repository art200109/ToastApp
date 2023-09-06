import json
import os
import socket
import subprocess
import sys
import urllib.request
from datetime import datetime
import win32evtlogutil
import win32evtlog
import logging
from logging.handlers import NTEventLogHandler
from logging.handlers import HTTPHandler
from flask.logging import default_handler
import requests
from flask import Flask, redirect, render_template, request, url_for

class CustomHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        url = "http://toast-splunk.westeurope.cloudapp.azure.com:8088/services/collector/event"
        #url = 'http://toast-monitor.westeurope.cloudapp.azure.com:8000/insert'
        print(log_entry)
        return requests.post(url, headers={"Content-type": "application/json","Authorization": "Splunk 0163e671-3e4f-45c5-8906-770c20e98408"},json={"table":"events", "server_name":"hosti", "_raw": log_entry}).content

root = logging.getLogger()

with open("codes.txt","r",encoding="utf8") as codes_file:
    codes = codes_file.readlines()

def create_minishift_url(service):
    return "http://"+service+"-toast."+minishift_ip+".nip.io"


def evt_log(message):
    DUMMY_EVT_APP_NAME = "Toast App"
    DUMMY_EVT_ID = 1234

    win32evtlogutil.ReportEvent(
        DUMMY_EVT_APP_NAME, DUMMY_EVT_ID,
        eventType=win32evtlog.EVENTLOG_ERROR_TYPE, strings=[message])


username = ""

minishift_ip = socket.gethostbyname("toast-mongo.westeurope.cloudapp.azure.com")


menu_url = create_minishift_url("menu")
login_url = create_minishift_url("login")
order_url = create_minishift_url("order")
inventory_url = create_minishift_url("inventory")

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

httpHandler = CustomHandler()

log = logging.getLogger('')

httpHandler.setLevel(logging.INFO)

# add handler to logger
log.addHandler(httpHandler)

@app.route("/home")
def home():
    if(username):
        with urllib.request.urlopen(menu_url) as url:
            foods = json.load(url)
        return render_template("user.html", foods=foods, username=username)
    return redirect(url_for('login'))


@app.route("/admin")
def admin():
    if(username):
        with urllib.request.urlopen(inventory_url) as url:
            foods = json.load(url)
        return render_template("admin.html", foods=foods, username=username)
    return redirect(url_for('login'))

# Route for handling the login page logic

@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def login():
    global username
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with urllib.request.urlopen(login_url+"/"+username) as url:
            user = json.load(url)
        if user is None or user == "null" or user["password"] != password:
            error = 'Invalid Credentials. Please try again.'
            evt_log(codes[0])
        else:
            if(user["role"] == "user"):
                return redirect(url_for('home'))
            else:
                return redirect(url_for('admin'))
    return render_template('login/dist/index.html', error=error)


@app.route("/order", methods=['POST'])
def order():
    data = request.get_json()
    data["username"] = username
    resp = requests.post(order_url, json=data)
    return (resp.content, resp.status_code, resp.headers.items())

@app.route("/update_inv", methods=['POST'])
def update_inv():
    data = request.get_json()

    resp = requests.put("{}/{}".format(inventory_url,data["product_name"]), json=data)
    return (resp.content, resp.status_code, resp.headers.items())


if __name__ == "__main__":
    app.run(debug=True)
