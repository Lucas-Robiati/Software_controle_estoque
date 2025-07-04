from Modules import *

class Database_conect:
    def __init__(self):
        self.cur = None
        self.conn = None
        self.create_database()
        self.create_tables()

    def get_db_connection(self):
        return psycopg2.connect(
            dbname=DBNAME,
            user=DBUSER,
            password=DBPASSWORD,
            host=DBHOST
        )

    def create_database(self):
        self.conn = self.get_db_connection()
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 
        self.cur = self.conn.cursor()

        DBNAME = "estoque"
        sql = (f"SELECT 'CREATE DATABASE {DBNAME}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{DBNAME}')")

        try:
            self.cur.execute(sql)
        except:
            self.cur.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(DBNAME)))

        self.cur.close()
        self.conn.close()

    def create_tables(self):
        self.conn = self.get_db_connection()
        self.cur  = self.conn.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS produtos " \
        "(id integer NOT NULL, nome varchar(60) NOT NULL, quantidade_es int NOT NULL, preco float NOT NULL)")
        self.conn.commit()

        self.cur.close()
        self.conn.close()

db = Database_conect()
#result = cur.fetchone()[0]
