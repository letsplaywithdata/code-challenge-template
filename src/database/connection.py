# import psycopg2
# import json
#
#
# def create_connection():
#     with open("config/config.json") as f:
#         config = json.load(f)
#     conn = psycopg2.connect(
#         host=config['db_creds'][0]['PGHOST'],
#         user=config['db_creds'][0]['PGUSER'],
#         password=config['db_creds'][0]['PGPASSWORD'],
#         database=config['db_creds'][0]['PGDATABASE']
#     )
#     print('Created Connection to database successfully')
#
#     return conn
#
#
# def close_connection(conn):
#     conn.close()

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

with open('config/config.json', 'r') as f:
    config = json.load(f)

db_creds = config['db_creds'][0]

engine = create_engine(
    f"postgresql://{db_creds['PGUSER']}:{db_creds['PGPASSWORD']}@{db_creds['PGHOST']}/{db_creds['PGDATABASE']}"
)
Session = sessionmaker(bind=engine)


class Connection:
    def __init__(self):
        self.session = Session()
        self.engine = engine

    def connect(self):
        return self.engine.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.session.rollback()
        self.session.close()
