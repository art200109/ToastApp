from flask import Flask, render_template, redirect, url_for, request
import os
import sqlite3
from operator import itemgetter
from itertools import groupby
import copy

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    db_connect = sqlite3.connect("fake_database.db")
    db_connect.row_factory = sqlite3.Row
    cursor = db_connect.cursor()
    cursor.execute("select * from cpu")
    sql_output = cursor.fetchall()

    cursor.close()
    db_connect.close()

    list_accumulator = []
    for item in sql_output:
        list_accumulator.append({k: item[k] for k in item.keys()})
        
    grouped_list = groupby(list_accumulator, key=itemgetter('server_name'))

    sums_dict = {}
    for key,value in grouped_list:
        leni = len(list(copy.deepcopy(value)))
        summi = sum(float(d['value']) for d in value)
        sums_dict[key] = float(summi/leni)

    return sums_dict


if __name__ == "__main__":
    app.run(debug=True)
