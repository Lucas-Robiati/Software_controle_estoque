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
        "(id SERIAL PRIMARY KEY NOT NULL, nome varchar(60) NOT NULL, quant_est int NOT NULL, quant_est_min int NOT NULL, preco_un float NOT NULL, preco_custo float NOT NULL)")
        self.conn.commit()

        self.execute_query("CREATE TABLE IF NOT EXISTS pessoa " \
        "(id SERIAL PRIMARY KEY, nome varchar(255) NOT NULL, telefone varchar(11), email varchar(255), CPF varchar(15) NOT NULL, cep varchar(9) NOT NULL)")
        self.conn.commit()

        self.execute_query("CREATE TABLE IF NOT EXISTS compra " \
        "(pessoa_id integer REFERENCES pessoa(id), quant_compra int NOT NULL, data DATE NOT NULL, produto_id integer REFERENCES produto(id))")
        self.conn.commit()

        self.close_connection()

    def add_pessoa(self, name:str, telefone:str, cpf:str, email:str, cep:str):
        self.get_db_connection()

        self.execute_query("SELECT CPF FROM pessoa WHERE CPF = %s", (cpf,))
        
        if (self.cur.fetchone() == None):
            self.execute_query("INSERT INTO pessoa (nome, telefone, email, CPF, cep) VALUES (%s, %s, %s, %s, %s)",(name, telefone, email, cpf, cep))
            self.conn.commit()
            self.close_connection()
            return None

        self.close_connection()
        return "CPF invalido - Usuario ja cadastrado"

    def add_produto(self, produto:str, quant:int, quant_min:int, preco_un:float, preco_cus:float):
        self.get_db_connection()
        
        self.execute_query("SELECT nome FROM produto WHERE nome = %s", (produto,))
        
        if (self.cur.fetchone() == None):
            self.execute_query("INSERT INTO produto (nome, quant_est, quant_est_min, preco_un, preco_custo) VALUES (%s, %s, %s, %s, %s)",(produto, quant, quant_min, preco_un, preco_cus))
            self.conn.commit()
            self.close_connection()
            return None

        self.close_connection()
        return "Produto ja cadastrado no sistema"

    def get_produtos(self):
        self.get_db_connection()
        self.execute_query("SELECT id, nome, quant_est, quant_est_min, preco_un, preco_custo FROM produto")
        resultados = self.cur.fetchall()
        self.close_connection()
        
        return resultados


    def update_produto(self, id=None, produto=None, new_preco_un=None, new_quant=None, new_preco_cus=None):

        if((produto == None) or (id != None)):
            self.get_db_connection()
            
            self.execute_query("SELECT id FROM produto WHERE id = %s", (id,))

            if (self.cur.fetchone() != None):
                if(new_quant):
                    self.execute_query("UPDATE produto SET quant_est = %s WHERE id = %s",(new_quant,id))
                    self.conn.commit()

                if(new_preco_un):
                    self.execute_query("UPDATE produto SET preco_un = %s WHERE id = %s",(new_preco_un,id))
                    self.conn.commit()
                
                if(new_preco_cus):
                    self.execute_query("UPDATE produto SET preco_custo = %s WHERE id = %s",(new_preco_cus,id))
                    self.conn.commit()
                
                self.close_connection()
                return
            
            else: 
                self.close_connection()
                return "ID de produto nao encontrado"

        if((id == None) and (produto != None)):
            self.get_db_connection()

            self.execute_query("SELECT nome FROM produto WHERE nome = %s", (produto,))
            
            if (self.cur.fetchone() != None):
                if(new_quant):
                    self.execute_query("UPDATE produto SET quant_est = %s WHERE nome = %s",(new_quant,produto))
                    self.conn.commit()

                if(new_preco_un):
                    self.execute_query("UPDATE produto SET preco_un = %s WHERE nome = %s",(new_preco_un,produto))
                    self.conn.commit()

                if(new_preco_cus):
                    self.execute_query("UPDATE produto SET preco_custo = %s WHERE nome = %s",(new_preco_cus,produto))
                    self.conn.commit()

                self.close_connection()
                return
            
            else: 
                self.close_connection()
                return "Produto nao encontrado"
        
        return "Identificadores vazios, coloque almenos um nome produto ou o id"


    def update_usuario(self, cpf=None, new_name=None, new_telefone=None, new_cpf=None, new_cep=None, new_email=None):

        self.get_db_connection()

        self.execute_query("SELECT CPF FROM pessoa WHERE CPF = %s", (cpf,))

        if (self.cur.fetchone() != None):
            if(new_name):
                self.execute_query("UPDATE pessoa SET nome = %s WHERE CPF = %s",(new_name,cpf))
                self.conn.commit()

            if(new_telefone):
                self.execute_query("UPDATE pessoa SET telefone = %s WHERE CPF = %s",(new_telefone,cpf))
                self.conn.commit()

            if(new_email):
                self.execute_query("UPDATE pessoa SET email = %s WHERE CPF = %s",(new_email,cpf))
                self.conn.commit()

            if(new_cpf):
                self.execute_query("UPDATE pessoa SET CPF = %s WHERE CPF = %s",(new_cpf,cpf))
                self.conn.commit()

            if(new_cep):
                self.execute_query("UPDATE pessoa SET cep = %s WHERE CPF = %s",(new_cep,cpf))
                self.conn.commit()

            self.close_connection()
            return
        
        else:
            self.close_connection()
            return "Pessoa nao encontrada"

#db = Database_conect()
#print(db.add_pessoa("Lucas Robiati","17996683675","lucas@gmail.com","477156358-63","15780-000"))
#db.update_usuario(cpf="477156358-63", new_name="Paulinho do Grau")
#db.add_produto("lima", 4, 3, 2.90, 0.50)
#print(db.update_produto(produto="limo",new_quant=420,new_preco=8.40))
