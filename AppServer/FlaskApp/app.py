from flask import Flask, render_template, redirect, url_for, request
import os
import urllib.parse, urllib.request, json 

username = ""

menu_url = "http://menu-toast.172.31.123.117.nip.io"
login_url = "http://login-toast.172.31.123.117.nip.io"
order_url = "http://order-toast.172.31.123.117.nip.io"

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
    data = urllib.parse.urlencode({ "product_id": request.args.get('product_id', None), "username": username }).encode()
    req =  urllib.request.Request(order_url, data=data) # this will make the method "POST"
    resp = urllib.request.urlopen(req)
    return resp
    
if __name__ == "__main__":
    app.run(debug=True)
