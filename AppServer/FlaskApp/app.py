from flask import Flask, render_template, redirect, url_for, request
import os
import urllib.request, json 

ocp_url = "http://toastapp-myproject.192.168.99.103.nip.io"

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

@app.route("/home")
def home():
    with urllib.request.urlopen(ocp_url+"/menu") as url:
        foods = json.load(url)
    return render_template("index.html",foods = foods)

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
    
if __name__ == "__main__":
    app.run()
