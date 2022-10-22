from flask import Flask, render_template, request
import os
import urllib.request, json 

ocp_url = "http://localhost:5000"

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

@app.route("/")
def home():
    with urllib.request.urlopen(ocp_url+"/menu") as url:
        foods = json.load(url)
    return render_template("index.html",foods = foods)
      
if __name__ == "__main__":
    app.run()