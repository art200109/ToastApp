from flask import Flask, render_template, redirect, url_for, request
import os
import urllib.request, json 

menu_url = "http://toastapp-myproject.192.168.99.103.nip.io/menu"
login_url = "http://login-myproject.192.168.99.103.nip.io/login"

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

@app.route("/home")
def home():
    with urllib.request.urlopen(menu_url) as url:
        foods = json.load(url)
    return render_template("index.html",foods = foods)

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
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
    
if __name__ == "__main__":
    app.run(debug=True)
