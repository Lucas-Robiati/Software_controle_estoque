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

def get_db_connection():
    return psycopg2.connect(
        dbname=DBNAME,
        user=DBUSER,
        password=DBPASSWORD,
        host=DBHOST
    )

conn = get_db_connection()

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
cur = conn.cursor()

DBNAME = "estoque"
sql = (f"SELECT 'CREATE DATABASE {DBNAME}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{DBNAME}')")

try:
    cur.execute(sql)
except:
    print("passou")
    cur.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(DBNAME)))

cur.close()
conn.close()

conn = get_db_connection()
cur  = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS produtos " \
"(id integer NOT NULL, nome varchar(60) NOT NULL, quantidade_es int NOT NULL, preco float NOT NULL)")
conn.commit()

cur.close()
conn.close()
#result = cur.fetchone()[0]
