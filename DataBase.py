from Modules import *

class Database_conect:
    def __init__(self):
        self.cur = None
        self.conn = None
        self.create_database()
        self.create_tables()

    def get_db_connection(self):
        try: 
            print(os.getenv('DBNAME'))
            self.conn = psycopg2.connect(
                dbname=os.getenv('DBNAME'),
                user=os.getenv('DBUSER'),
                password=os.getenv('DBPASSWORD'),
                host=os.getenv('DBHOST')
            )
            self.cur = self.conn.cursor()
            print("Conexão Estabelecida")
        
        except psycopg2.Error as e:
            print(f"Erro ao conectar: {e}")
            self.conn = None
            self.cur = None
    
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

        os.environ['DBNAME'] = "estoque"

        # Verifica se o data base ja existe
        query = (f"SELECT 'CREATE DATABASE {os.getenv('DBNAME')}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{os.getenv('DBNAME')}')")

        self.execute_query(query)
        msg = self.cur.fetchone()

        if( msg != None):
            print("DataBase estoque Criada")
            self.execute_query(sql.SQL('CREATE DATABASE {}').format(sql.Identifier(os.getenv('DBNAME'))))
        
        self.close_connection()

    def create_tables(self):
        self.get_db_connection()

        # Criando Tabelas
        self.execute_query("CREATE TABLE IF NOT EXISTS produto " \
        "(id SERIAL PRIMARY KEY NOT NULL, nome varchar(60) NOT NULL, quant_est int NOT NULL, preco_un float NOT NULL)")
        self.conn.commit()

        self.execute_query("CREATE TABLE IF NOT EXISTS pessoa " \
        "(id SERIAL PRIMARY KEY, nome varchar(255) NOT NULL, telefone varchar(11), CPF varchar(12) NOT NULL)")
        self.conn.commit()

        self.execute_query("CREATE TABLE IF NOT EXISTS compra " \
        "(pessoa_id integer REFERENCES pessoa(id), quant_compra int NOT NULL, data DATE NOT NULL, produto_id integer REFERENCES produto(id))")
        self.conn.commit()

        self.close_connection()

    def add_pessoa(self, name:str, telefone:str, cpf:str):
        self.get_db_connection()

        self.execute_query("SELECT CPF FROM pessoa WHERE CPF = %s", (cpf,))
        
        if (self.cur.fetchone() == None):
            self.execute_query("INSERT INTO pessoa (nome, telefone, CPF) VALUES (%s, %s, %s)",(name, telefone, cpf))
            self.conn.commit()

            self.close_connection()
            return None

        self.close_connection()
        return "CPF invalido - Usuario ja cadastrado"

    def add_produto(self, produto:str, quant:int, preco:float):
        self.get_db_connection()

        self.execute_query("INSERT INTO produto (nome, quant_est, preco_un) VALUES (%s, %s, %s)",(produto, quant, preco))
        self.conn.commit()

        self.close_connection()

db = Database_conect()
db.add_pessoa("Lucas Robiati","17996683675","477156358-63")

#db.add_produto("lima", 4, 2.90)
#result = cur.fetchone()[0]
