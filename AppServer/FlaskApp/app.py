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

class CustomHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        url = 'http://toast-monitor.westeurope.cloudapp.azure.com:8000/insert'
        print(log_entry)
        return requests.post(url, headers={"Content-type": "application/json"},json={"table":"events", "server_name":"hosti", "value": log_entry}).content

root = logging.getLogger()

with open("codes.csv","r") as codes_file:
    codes = codes_file.readlines()



import requests
from flask import Flask, redirect, render_template, request, url_for


def create_minishift_url(service):
    return "http://"+service+"-toast."+minishift_ip+".nip.io"


def log(message):
    logging.debug("debug log")
    DUMMY_EVT_APP_NAME = "Toast App"
    DUMMY_EVT_ID = 1234

    win32evtlogutil.ReportEvent(
        DUMMY_EVT_APP_NAME, DUMMY_EVT_ID,
        eventType=win32evtlog.EVENTLOG_ERROR_TYPE, strings=[message])


username = ""

minishift_ip = socket.gethostbyname("toast-ocp.westeurope.cloudapp.azure.com")


menu_url = create_minishift_url("menu")
login_url = create_minishift_url("login")
order_url = create_minishift_url("order")

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

http_handler = CustomHandler()

app.logger.addHandler(http_handler)
root.addHandler(default_handler)
root.addHandler(http_handler)

@app.route("/home")
def home():
    with urllib.request.urlopen(menu_url) as url:
        foods = json.load(url)
    return render_template("index.html", foods=foods, username=username)

# Route for handling the login page logic


@app.route('/', methods=['GET', 'POST'])
def login():
    global username
    log()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        with urllib.request.urlopen(login_url+"/"+username) as url:
            user = json.load(url)
        if user == "null" or user["password"] != password:
            error = 'Invalid Credentials. Please try again.'
            log(codes[0])
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route("/order", methods=['POST'])
def order():
    data = request.get_json()
    data["username"] = username
    resp = requests.post(order_url, json=data)
    return (resp.content, resp.status_code, resp.headers.items())


if __name__ == "__main__":
    app.run(debug=True)
