from flask import Flask, render_template, redirect, url_for, request
import os
import sqlite3
from operator import itemgetter
from itertools import groupby
import copy

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)

def get_avg_by_server(metric,groupby="server_name"):
    db_connect = sqlite3.connect("fake_database.db")
    db_connect.row_factory = sqlite3.Row
    cursor = db_connect.cursor()
    cursor.execute("select server_name,avg(value) from {} group by {}".format(metric,groupby))
    sql_output = cursor.fetchall()

    cursor.close()
    db_connect.close()
    print(sql_output)

    list_accumulator = []
    for item in sql_output:
        list_accumulator.append({k: item[k] for k in item.keys()})
    
    return list_accumulator


# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    metrics = { "cpu":{},"memory":{}}
    for key in metrics:
        metrics[key] = get_avg_by_server(key)
    
    metrics["disk"] = get_avg_by_server("disk","server_name, disk_name")
    
    return metrics


if __name__ == "__main__":
    app.run(debug=True)
