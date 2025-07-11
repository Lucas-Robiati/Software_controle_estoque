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
            self.execute_query(sql.SQL('CREATE DATABASE {}').format(sql.SQL(os.getenv('DBNAME'))))
        
        self.close_connection()

    def create_tables(self):

        self.get_db_connection()

        queries = [
            """CREATE TABLE IF NOT EXISTS produto (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(60) NOT NULL,
                quant_est INT NOT NULL,
                quant_est_min INT NOT NULL,
                preco_un FLOAT NOT NULL,
                preco_custo FLOAT NOT NULL
            )""",

            """CREATE TABLE IF NOT EXISTS pessoa (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                telefone VARCHAR(11),
                email VARCHAR(255),
                CPF VARCHAR(15) NOT NULL,
                cep VARCHAR(9) NOT NULL
            )""",

            """CREATE TABLE IF NOT EXISTS venda (
                id SERIAL PRIMARY KEY,
                pessoa_id INT REFERENCES pessoa(id),
                data TIMESTAMP NOT NULL
            )""",

            """CREATE TABLE IF NOT EXISTS produto_venda (
                venda_id INT REFERENCES venda(id) ON DELETE CASCADE,
                produto_id INT REFERENCES produto(id) ON DELETE CASCADE,
                quant_compra INT NOT NULL,
                valor_unit FLOAT NOT NULL
            )""",

            """CREATE OR REPLACE VIEW relatorio_vendas AS
                SELECT 
                    v.id AS id_venda,
                    v.data::DATE AS data_venda,
                    p.cpf AS cpf_cliente,
                    pr.nome AS produto,
                    pv.quant_compra AS quantidade,
                    pv.valor_unit
                FROM 
                    venda v
                JOIN 
                    pessoa p ON v.pessoa_id = p.id
                JOIN 
                    produto_venda pv ON v.id = pv.venda_id
                JOIN 
                    produto pr ON pv.produto_id = pr.id
                ORDER BY 
                    v.data DESC"""

        ]

        for query in queries:   
            try:
                self.cur.execute(query)
                self.conn.commit()
            except psycopg2.Error as e:
                print(f"Erro criando tabelas: {e}")
                self.conn.rollback()

        self.close_connection()

    def get_relatorio_vendas(self):
        self.get_db_connection()
        self.execute_query("SELECT * FROM relatorio_vendas")
        resultados = self.cur.fetchall()
        self.close_connection()
        return resultados


    def add_pessoa(self, name:str, telefone:str, email:str, cpf:str, cep:str):
        self.get_db_connection()

        self.execute_query("SELECT CPF FROM pessoa WHERE CPF = %s", (cpf,))
        
        if (self.cur.fetchone() == None):
            self.execute_query("INSERT INTO pessoa (nome, telefone, email, CPF, cep) VALUES (%s, %s, %s, %s, %s)",(name, telefone, email, cpf, cep))
            self.conn.commit()
            self.close_connection()
            return None

        self.close_connection()
        return "CPF invalido - Usuario ja cadastrado"

    def listar_clientes(self):
        self.get_db_connection()
        self.execute_query("SELECT nome, telefone, email, CPF, cep FROM pessoa")
        resultados = self.cur.fetchall()
        self.close_connection()
        return resultados

    def excluir_cliente(self, cpf:str):
        self.get_db_connection()

        self.execute_query("SELECT id FROM pessoa WHERE CPF = %s", (cpf,))
        if self.cur.fetchone() is None:
            self.close_connection()
            return "Cliente não encontrado"

        self.execute_query("DELETE FROM pessoa WHERE CPF = %s", (cpf,))
        self.conn.commit()
        self.close_connection()
        return None

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

    def new_venda(self, produto: dict, cpf: str):
        self.get_db_connection()

        # Verifica se cliente existe
        self.execute_query("SELECT id FROM pessoa WHERE cpf = %s", (cpf,))
        resultado_cliente = self.cur.fetchone()
        if resultado_cliente is None:
            self.close_connection()
            return "Usuário sem cadastro"

        pessoa_id = resultado_cliente[0]

        # Verifica se há estoque suficiente
        for nome_produto, quantidade in produto.items():
            self.execute_query("SELECT quant_est FROM produto WHERE nome = %s", (nome_produto,))
            estoque = self.cur.fetchone()
            if estoque is None:
                self.close_connection()
                return f"Produto '{nome_produto}' não encontrado"
            if estoque[0] < quantidade:
                self.close_connection()
                return f"Produto '{nome_produto}' não tem esta quantidade em estoque"

        # Cria venda e obtém ID com RETURNING
        self.execute_query("INSERT INTO venda (pessoa_id, data) VALUES (%s, NOW()) RETURNING id", (pessoa_id,))
        venda_id = self.cur.fetchone()[0]

        # Para cada produto, registra venda e atualiza estoque
        for nome_produto, quantidade in produto.items():
            self.execute_query("SELECT id, preco_un FROM produto WHERE nome = %s", (nome_produto,))
            resultado_prod = self.cur.fetchone()
            produto_id, valor_unitario = resultado_prod

            # Insere na tabela produto_venda com valor_unitario
            self.execute_query("""
                INSERT INTO produto_venda (venda_id, produto_id, quant_compra, valor_unit)
                VALUES (%s, %s, %s, %s)
            """, (venda_id, produto_id, quantidade, valor_unitario))

            # Atualiza estoque
            self.execute_query("""
                UPDATE produto SET quant_est = quant_est - %s WHERE id = %s
            """, (quantidade, produto_id))

        self.conn.commit()
        self.close_connection()


    def get_produtos(self):
        self.get_db_connection()
        self.execute_query("SELECT id, nome, quant_est, quant_est_min, preco_un, preco_custo FROM produto")
        resultados = self.cur.fetchall()
        self.close_connection()
        
        return resultados


    def update_produto(self, id=None, produto=None, new_nome=None, new_preco_un=None, new_quant=None, new_estoque_min=None, new_preco_cus=None):

        if (produto is None) or (id is not None):
            self.get_db_connection()
    
            self.execute_query("SELECT id FROM produto WHERE id = %s", (id,))
    
            if self.cur.fetchone() is not None:
                if new_nome:
                    self.execute_query("UPDATE produto SET nome = %s WHERE id = %s", (new_nome, id))
                    self.conn.commit()
    
                if new_quant:
                    self.execute_query("UPDATE produto SET quant_est = %s WHERE id = %s", (new_quant, id))
                    self.conn.commit()
    
                if new_estoque_min:
                    self.execute_query("UPDATE produto SET quant_est_min = %s WHERE id = %s", (new_estoque_min, id))
                    self.conn.commit()
    
                if new_preco_un:
                    self.execute_query("UPDATE produto SET preco_un = %s WHERE id = %s", (new_preco_un, id))
                    self.conn.commit()
    
                if new_preco_cus:
                    self.execute_query("UPDATE produto SET preco_custo = %s WHERE id = %s", (new_preco_cus, id))
                    self.conn.commit()
    
                self.close_connection()
                return
    
            else:
                self.close_connection()
                return "ID de produto nao encontrado"
    
        if (id is None) and (produto is not None):
            self.get_db_connection()
    
            self.execute_query("SELECT nome FROM produto WHERE nome = %s", (produto,))
    
            if self.cur.fetchone() is not None:
                if new_nome:
                    self.execute_query("UPDATE produto SET nome = %s WHERE nome = %s", (new_nome, produto))
                    self.conn.commit()
    
                if new_quant:
                    self.execute_query("UPDATE produto SET quant_est = %s WHERE nome = %s", (new_quant, produto))
                    self.conn.commit()
    
                if new_estoque_min:
                    self.execute_query("UPDATE produto SET estoque_min = %s WHERE nome = %s", (new_estoque_min, produto))
                    self.conn.commit()
    
                if new_preco_un:
                    self.execute_query("UPDATE produto SET preco_un = %s WHERE nome = %s", (new_preco_un, produto))
                    self.conn.commit()
    
                if new_preco_cus:
                    self.execute_query("UPDATE produto SET preco_custo = %s WHERE nome = %s", (new_preco_cus, produto))
                    self.conn.commit()
    
                self.close_connection()
                return
    
            else:
                self.close_connection()
                return "Produto nao encontrado"
    
        return "Identificadores vazios, coloque almenos um nome produto ou o id"

    def aumentar_estoque(self, produto, quant_aumentar):
        self.get_db_connection()

        self.execute_query("SELECT quant_est FROM produto WHERE nome = %s", (produto,))
        resultado = self.cur.fetchone()
        if resultado is None:
            self.close_connection()
            return f"Produto '{produto}' não encontrado."

        quant_atual = resultado[0] or 0
        nova_quant = quant_atual + quant_aumentar

        self.execute_query("UPDATE produto SET quant_est = %s WHERE nome = %s", (nova_quant, produto))
        self.conn.commit()
        self.close_connection()
        return None


    def remove_produto(self, id: int = None, produto: str = None):
        if id is None and produto is None:
            return "Identificadores vazios, forneça o ID ou o nome do produto"
    
        self.get_db_connection()
    
        if id is not None:
            self.execute_query("SELECT id FROM produto WHERE id = %s", (id,))
            if self.cur.fetchone() is not None:
                self.execute_query("DELETE FROM produto WHERE id = %s", (id,))
                self.conn.commit()
                self.close_connection()
                return None
            else:
                self.close_connection()
                return "ID não encontrado"
    
        if produto is not None:
            self.execute_query("SELECT nome FROM produto WHERE nome = %s", (produto,))
            if self.cur.fetchone() is not None:
                self.execute_query("DELETE FROM produto WHERE nome = %s", (produto,))
                self.conn.commit()
                self.close_connection()
                return None
            else:
                self.close_connection()
                return "Produto não encontrado"


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

    def cliente_existe(self, cpf):
        self.get_db_connection()
        self.execute_query("SELECT 1 FROM pessoa WHERE cpf = %s", (cpf,))
        return self.cur.fetchone() is not None


    def remove_usuario(self, cpf:str):

        self.get_db_connection()

        self.execute_query("SELECT CPF FROM pessoa WHERE CPF = %s", (cpf,))
        
        if (self.cur.fetchone() != None):
            self.execute_query("DELETE FROM pessoa WHERE CPF = %s", (cpf,))
            self.conn.commit()

        else:
            self.close_connection()
            return "Pessoa nao encontrada"
    
    def remove_produto(self, id:int=None, produto:str=None):
        
        if((produto == None) or (id != None)):
            self.get_db_connection()
            
            self.execute_query("SELECT id FROM produto WHERE id = %s", (id,))

            if (self.cur.fetchone() != None):
                self.execute_query("DELETE FROM produto WHERE id = %s", (id,))
                self.conn.commit()
                self.close_connection()
                return
        
            else:
                self.close_connection()
                return "ID nao encontrado"

        if((id == None) and (produto != None)):
            self.get_db_connection()

            self.execute_query("SELECT nome FROM produto WHERE nome = %s", (produto,))
            
            if (self.cur.fetchone() != None):
                self.execute_query("DELETE FROM produto WHERE nome = %s", (produto,))
                self.conn.commit()
                self.close_connection()
                return
        
            else:
                self.close_connection()
                return "Produto nao encontrada"

        return "Identificadores vazios, coloque almenos um nome produto ou o id"

venda = {'lima': 5}
db = Database_conect()
db.add_pessoa("Lucas Robiati","17996683675","lucas@gmail.com","477.156.358-63","15780-000")
db.add_produto("lima", 4, 2, 2.90, 0.50)
print(db.new_venda(venda,"477.156.358-63"))
