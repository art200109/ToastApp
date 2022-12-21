import sys, os
from datetime import datetime
import sqlite3, json
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware 


folder_path = os.path.dirname(__file__)
sys.path.insert(1, folder_path)

DB = 'databast.db'

# DATA BASE
class DataBase():

    def __init__(self) -> None:
        """
            This database works with JSON format
        """
        self.tables = ['cpu','memory','disk_space','events']
        self.create_tables()

    def create_tables(self):
            """
                Create the tables inside the database
            """
            db_connect = sqlite3.connect(DB)
            cursor = db_connect.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS cpu (
                                server_name TEXT PRIMARY KEY NOT NULL,
                                value TEXT NOT NULL
                                )""")
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS memory (
                                server_name TEXT PRIMARY KEY NOT NULL,
                                value TEXT NOT NULL
                                )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS disk_space (
                                server_name TEXT PRIMARY KEY NOT NULL,
                                disk_name TEXT NOT NULL,
                                value TEXT NOT NULL
                                )""")

            cursor.execute("""CREATE TABLE IF NOT EXISTS events (
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
        if table in self.tables:
            db_connect = sqlite3.connect(DB)
            cursor = db_connect.cursor()
            
            cursor.execute(f"SELECT *, oid  FROM {table}")
            results = cursor.fetchall()

            cursor.close()
            db_connect.close()

            return results
        else:
            raise Exception(f'table {table} does not exist')

    def insert(self, payload: json):
        """
        This function insert rows into db table
        
        Parameters
        ----------
        payload: json
            the data inside JSON request {table={'cpu', 'memory', 'disk_space', 'events'} , server_name, value}

        """
        db_connect = sqlite3.connect(DB)
        cursor = db_connect.cursor()

        payload['value'] = (f'time_stamp: {datetime.now().strftime("%d/%m/%y %H:%M:%S.%f")} | value: {payload.get("value")}')

        try:
            if payload['table'] == 'cpu':
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:server_name, :value)",
                                            {
                                            'server_name': payload.get('server_name'),
                                            'value': payload.get('value')
                                            })
            elif payload['table'] == 'memory':
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:server_name, :value)",
                                            {
                                            'server_name': payload.get('server_name'),
                                            'value': payload.get('value')
                                            })
            elif payload['table'] == 'disk_space':
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:server_name, :disk_name, :value)",
                                            {
                                            'server_name': payload.get('server_name'),
                                            'value': payload.get('value'),
                                            'disk_name': payload.get('disk_name')
                                            })
            elif payload['table'] == 'events':
                cursor.execute(f"INSERT INTO {payload['table']} VALUES (:value)",
                                            {
                                            'value': payload.get('value')
                                            })
            else:
                raise Exception(f'table {payload["table"]} does not exist')
        except:
            pass
        
        db_connect.commit()
        cursor.close()
        db_connect.close()

        
class APIService:
    def run(self):
        uvicorn.run('API_Server:app', host='0.0.0.0', port=8000, log_level='info')

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = DataBase()
service = APIService()
service.run()

@app.get("/")
async def root():
    return print(f'Just a page')

@app.get("/fetch/table={table}")
async def fetch(table: str):
    return db.fetch(table)

@app.post("/insert")
async def post_request(request: Request):
    # db.POST_reminders(payload=payload)
    payload = await request.json()
    return db.insert(payload)
    # raise HTTPException(status_code=404, detail="URL path not found")