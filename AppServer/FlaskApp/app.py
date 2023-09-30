import json
import os
import socket
import urllib.request
import win32evtlogutil
import win32evtlog
import requests
import configparser
from flask import Flask, redirect, render_template, request, url_for
from googletrans import Translator
from urllib.parse import quote_plus


translator = Translator()

AGENT_CONFIG_FILE = r'C:\inetpub\wwwroot\ToastApp\MonitoringAgent\agent.conf'
#log_url = "https://toast-splunk.westeurope.cloudapp.azure.com:8088/services/collector/raw"
log_url = "http://toast-monitor.westeurope.cloudapp.azure.com:8000/insert"

def log(content):
        config = configparser.ConfigParser()
        config.read(AGENT_CONFIG_FILE)

        log_url =  config["default"]["destination"]
        auth = config["default"]["authorization"]

        print(content)
        return requests.post(
                            log_url, 
                            headers={
                                "Content-type": "application/json",
                                "Authorization": auth
                            },
                            json={
                                "table":"events", 
                                "server_name":"toast-app.westeurope.cloudapp.azure.com",
                                "event": json.loads(content)
                            },
                            verify=False
        ).content


def create_minishift_url(service):
    return "http://"+service+"-toast."+minishift_ip+".nip.io"

def evt_log(message):
    DUMMY_EVT_APP_NAME = "Toast App"
    DUMMY_EVT_ID = 1234
    message = translator.translate(message, dest="he").text

    win32evtlogutil.ReportEvent(
        DUMMY_EVT_APP_NAME, DUMMY_EVT_ID,
        eventType=win32evtlog.EVENTLOG_ERROR_TYPE, strings=[message])


with open("codes.txt","r",encoding="utf8") as codes_file:
    codes = codes_file.readlines()
    
username = ""

minishift_ip = socket.gethostbyname("toast-ocp.westeurope.cloudapp.azure.com")


menu_url = create_minishift_url("menu")
login_url = create_minishift_url("login")
order_url = create_minishift_url("order")
inventory_url = create_minishift_url("inventory")

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

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
            if user is None or user == "null":
                reason = 'User does not exist'
            else:
                reason = 'Wrong password'
            error = reason + ", Please try again."

            login_evt = {
                "type": "login",
                "status": "failure",
                "user": username,
                "reason": reason
            }
            log(json.dumps(login_evt))
            evt_log(codes[0])
        else:
            login_evt = {
                "type": "login",
                "status": "success",
                "user": username,
                "role": user["role"]
            }
            log(json.dumps(login_evt))
            evt_log(codes[1].format(username))

            if(user["role"] == "user"):
                return redirect(url_for('home'))
            else:
                return redirect(url_for('admin'))
    return render_template('login/dist/index.html', error=error)


@app.route("/order", methods=['POST'])
def order():
    data = request.get_json()
    data["username"] = username
    product_name = data["product_name"]

    resp = requests.post(order_url, json=data)
    
    # Log
    status = "success" if resp.ok else "failure"

    order_evt = {
                "type": "order",
                "status": status,
                "user": username,
                "product_name": product_name
    }
    log(json.dumps(order_evt))

    if(resp.ok):
        evt_log(codes[2].format(username, product_name))
    else:
        evt_log(codes[3].format(username, product_name))


    return (resp.content, resp.status_code, resp.headers.items())

@app.route("/update_inv", methods=['POST'])
def update_inv():
    data = request.get_json()
    product_name = data["product_name"]
    resp = requests.put("{}/{}".format(inventory_url,quote_plus(product_name)), json=data)

    
    # Log
    status = "success" if resp.ok else "failure"

    order_evt = {
                "type": "inventory fill",
                "status": status,
                "user": username,
                "delta": data["delta"],
                "product_name": product_name
    }
    log(json.dumps(order_evt))

    if(resp.ok):
        evt_log(codes[4].format(product_name))
    else:
        evt_log(codes[5].format(product_name))
        
    return (resp.content, resp.status_code, resp.headers.items())


if __name__ == "__main__":
    app.run(debug=True)