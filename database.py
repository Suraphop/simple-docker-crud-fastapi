from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os 

load_dotenv()

servername = os.getenv('SERVERNAME')
dbname = os.getenv('DBNAME')
id = os.getenv('id')
password = os.getenv('PASSWORD')

SQLALCHEMY_DATABASE_URL = 'mssql+pyodbc://sa:'+password+'@' + servername + '/' + dbname + '?driver=ODBC+Driver+17+for+SQL+Server'


engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()