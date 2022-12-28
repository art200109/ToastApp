from flask import Flask, render_template, redirect, url_for, request
import os
import sqlite3
import sys

template_dir = os.path.dirname(__file__)
app = Flask(__name__, template_folder=template_dir)
path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

def get_avg_by_server(metric,groupby="server_name"):
    db_connect = sqlite3.connect(os.path.join(os.path.dirname(path),"API","fake_database.db"))
    db_connect.row_factory = sqlite3.Row
    cursor = db_connect.cursor()
    cursor.execute("select {},avg(value) from {} group by {}".format(groupby,metric,groupby))
    sql_output = cursor.fetchall()

    cursor.close()
    db_connect.close()

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
    
    disk_stats = get_avg_by_server("disk","server_name, disk_name")
    fixed_disk_stats = {}
    for server in disk_stats:
        if(server["server_name"] not in fixed_disk_stats):
            fixed_disk_stats[server["server_name"]] = []
        fixed_disk_stats[server["server_name"]].append("{} - {}".format(server["disk_name"], server["avg(value)"]))

    db_connect = sqlite3.connect(os.path.join(os.path.dirname(path),"API","fake_database.db"))
    db_connect.row_factory = sqlite3.Row
    cursor = db_connect.cursor()
    cursor.execute("select * from events")
    events = cursor.fetchall()
    parsed_events = []
    for item in events:
        parsed_events.append({k: item[k] for k in item.keys()})

    cursor.close()
    db_connect.close()
    return render_template("index.html", metrics=metrics, disk_stats=fixed_disk_stats,events=parsed_events)


if __name__ == "__main__":
    app.run(debug=True)
