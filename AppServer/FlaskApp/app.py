from flask import Flask, render_template, redirect, url_for, request
import os
import sys
import urllib.request, json
import requests
from datetime import datetime
import subprocess

def create_minishift_url(service):
    return "http://"+service+"-toast."+minishift_ip+".nip.io"


username = ""
#p = subprocess.Popen("minishift ip", stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL)
#out, err = p.communicate()
#minishift_ip = out.decode(sys.stdout.encoding).strip()
minishift_ip = "192.168.99.101"


menu_url = create_minishift_url("menu")
login_url = create_minishift_url("login")
order_url = create_minishift_url("order")

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

@app.route("/home")
def home():
    with urllib.request.urlopen(menu_url) as url:
        foods = json.load(url)
    return render_template("index.html",foods = foods, username=username)

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    global username
    error = None
    if request.method == 'POST':  
        username = request.form['username']
        password = request.form['password']
        
        with urllib.request.urlopen(login_url+"/"+username) as url:
            user = json.load(url)
        if user == "null" or user["password"] != password:
            error = 'Invalid Credentials. Please try again.'
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
