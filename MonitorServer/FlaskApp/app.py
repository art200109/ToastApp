from flask import Flask, render_template, redirect, url_for, request
import os
import sqlite3
from operator import itemgetter
from itertools import groupby

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)
db_connect = sqlite3.connect("fake_database.db")
cursor = db_connect.cursor()
cursor.execute("select * from cpu")
temp = cursor.fetchall()
temp = groupby(temp, key=itemgetter('server_name'))
cursor.close()
db_connect.close()

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    return temp
       
if __name__ == "__main__":
    app.run(debug=True)
