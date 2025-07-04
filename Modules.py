import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
from dotenv import load_dotenv
import os

load_dotenv()

DBNAME = os.getenv('DBNAME', 'postgres')
DBUSER = os.getenv('DBUSER', 'postgres')
DBPASSWORD = os.getenv('DBPASSWORD', 'postgres')
DBHOST = os.getenv('DBHOST', 'localhost')