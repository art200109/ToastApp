import sys, os
import sqlite3, json
import uvicorn
import threading
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware 
from datetime import datetime

folder_path = os.path.dirname(__file__)
sys.path.insert(1, folder_path)

tables_list = ['cpu','memory','disk','events']

# DATA BASE
class DataBase():

    def __init__(self, tables: list) -> None:
        """
            This database works with JSON format
        """
        self.db_name = 'fake_database.db'
        self.tables = tables
        self.create_tables()

    def create_tables(self):
            """
                Create the tables inside the database
            """
            db_connect = sqlite3.connect(self.db_name)
            cursor = db_connect.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS cpu (
                                time_stamp TEXT NOT NULL,
                                server_name TEXT NOT NULL,
                                value TEXT NOT NULL
                                )""")
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS memory (
                                time_stamp TEXT NOT NULL,
                                server_name TEXT NOT NULL,
                                value TEXT NOT NULL
                                )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS disk (
                                time_stamp TEXT NOT NULL,
                                server_name TEXT NOT NULL,
                                disk_name TEXT NOT NULL,
                                value TEXT NOT NULL
                                )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS events (
                                time_stamp TEXT NOT NULL,
                                value TEXT PRIMARY KEY NOT NULL
                                )""")
            
            cursor.close()
            db_connect.close()

    def fetch(self, table: str):
        """
            This function fetch rows from db table
        
        Parameters
        ----------
        payload: json
            the data inside JSON request {table, server_name, value}

        """
        db_connect = sqlite3.connect(self.db_name)
        cursor = db_connect.cursor()
        
        cursor.execute(f"SELECT oid, * FROM {table}")
        results = cursor.fetchall()

        cursor.close()
        db_connect.close()

        return results

    def insert(self, payload: json):
        """
        This function insert rows into db table
        
        Parameters
        ----------
        payload: json
            the data inside JSON request {table={'cpu', 'memory', 'disk_space', 'events'} , server_name, value}

        """
        db_connect = sqlite3.connect(self.db_name)
        cursor = db_connect.cursor()

        try:
            if payload['table'] == 'cpu':
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:time_stamp, :server_name, :value)",
                                            {
                                            'time_stamp': datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"),
                                            'server_name': payload.get('server_name'),
                                            'value': payload.get('value')
                                            })
            elif payload['table'] == 'memory':
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:time_stamp, :server_name, :value)",
                                            {
                                            'time_stamp': datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"),
                                            'server_name': payload.get('server_name'),
                                            'value': payload.get('value')
                                            })
            elif payload['table'] == 'disk_space':
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:time_stamp ,:server_name, :disk_name, :value)",
                                            {
                                            'time_stamp': datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"),
                                            'server_name': payload.get('server_name'),
                                            'value': payload.get('value'),
                                            'disk_name': payload.get('disk_name')
                                            })
            else: 
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:time_stamp, :value)",
                                            {
                                            'time_stamp': datetime.now().strftime("%d/%m/%y %H:%M:%S.%f"),
                                            'value': payload.get('value')
                                            })

        except:
            pass
        
        db_connect.commit()
        cursor.close()
        db_connect.close()

class API_Server():
    def run_uvicorn(self):
        uvicorn.run(app='api_server:app', host='0.0.0.0', log_level='info')

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
                )

@app.get("/")
async def root():
    return 'Just a page'
  
@app.get("/fetch/table={table}")
async def fetch_queries(table: str):
    if table in tables_list:
        return db.fetch(table)
    else:
        f'table "{table}" does not exist'

@app.post("/insert")
async def post_query(request: Request):
    payload = await request.json()
    if payload['table'] in tables_list:
        return db.insert(payload)
    else:
        f'table "{request["table"]}" does not exist'

db = DataBase(tables=tables_list)
api = API_Server()

start_api_thread = threading.Thread(target=api.run_uvicorn)
start_api_thread.start()