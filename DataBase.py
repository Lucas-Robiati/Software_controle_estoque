from Modules import *

class Database_conect:
    def __init__(self):
        self.cur = None
        self.conn = None
        self.create_database()
        self.create_tables()

    def get_db_connection(self):
        try: 
            self.conn = psycopg2.connect(
                dbname=DBNAME,
                user=DBUSER,
                password=DBPASSWORD,
                host=DBHOST
            )
            self.cur = self.conn.cursor()
            print("Conexão Estabelecida")
        
        except psycopg2.Error as e:
            print(f"Erro ao conectar: {e}")
            self.connection = None
            self.cursor = None
    
    def execute_query(self, query, params=None):
        if not self.cur:
            print("cur não inicializado. Conecte-se ao banco de dados primeiro.")
            return None

        try:
            if params:
                self.cur.execute(query, params)
            else:
                self.cur.execute(query)
            return self.cur
        except psycopg2.Error as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
    
    def close_connection(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Conexão fechada.")

    def create_database(self):
        self.get_db_connection()
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 

        DBNAME = "estoque"
        # Verifica se o data base ja existe
        sql = (f"SELECT 'CREATE DATABASE {DBNAME}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{DBNAME}')")

        try:
            self.execute_query(sql)
        except:
            self.cur.execute(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(DBNAME)))
        
        self.close_connection()

    def create_tables(self):
        self.get_db_connection()

        self.execute_query("CREATE TABLE IF NOT EXISTS produtos " \
        "(id integer NOT NULL, nome varchar(60) NOT NULL, quantidade_compra int NOT NULL, preco_un float NOT NULL)")
        self.conn.commit()

        self.close_connection()

db = Database_conect()
#result = cur.fetchone()[0]
