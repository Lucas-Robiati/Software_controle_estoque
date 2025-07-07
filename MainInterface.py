from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from DataBase import *
from Modules import *

class Application(Validate):
  def __init__(self, root:'Tk'):
    self.root = root
    self.banco_dados = Database_conect()                             
    self.window()                                  
    root.mainloop()  

  def window(self):
  # Funcao da janela principal
    self.root.title("Controle de Estoque")                       # Nome do software
    self.root.configure(background= Color.white.value)           # Background da janela principal
    self.root.geometry("950x520")                                # Geometria da janela 
    self.root.minsize(width=950, height=520)                     # Tamanho minimo da janela 
    self.root.resizable(True,True)                               # Software pode redimensionar 
    self.root.protocol('WM_DELETE_WINDOW', self.destroy_window)
    self.layout_sidebar()
    self.layout_header()
    self.layout_produtos()

  def layout_sidebar(self):
    self.root.grid_rowconfigure(0, weight=1)
    self.sidebar = Frame(root, background=Color.light_blue.value, width=150)
    self.sidebar.grid_columnconfigure(0, weight=1)
    self.sidebar.grid(row=0, column=0, sticky="ns")
    self.sidebar.grid_propagate(False)

    self.btn_produtos = self.create_button(self.sidebar, "Produtos", command_func=self.layout_produtos)
    self.btn_entrada = self.create_button(self.sidebar, "Entradas", command_func=None)
    self.btn_saida = self.create_button(self.sidebar, "Saidas", command_func=None)
    self.btn_cliente = self.create_button(self.sidebar, "Clientes", command_func=None)
    
  def layout_header(self):
    self.root.grid_columnconfigure(1, weight=1)
    self.root.grid_rowconfigure(0, weight=1)

    self.frame_principal = Frame(self.root, background=Color.white.value)
    self.frame_principal.grid(row=0, column=1, sticky="nsew")

    self.frame_principal.grid_rowconfigure(1, weight=1)
    self.frame_principal.grid_columnconfigure(0, weight=1)

    self.header = Frame(self.frame_principal, height=50, background=Color.aqua_blue.value)
    self.header.grid(row=0, column=0, sticky="ew")


  def layout_produtos(self):
    self.grid_produto = Frame(self.frame_principal, background=Color.white.value)
    self.grid_produto.grid(row=1, column=0, sticky="nsew", padx=100, pady=75)
    self.frame_principal.grid_rowconfigure(1, weight=1)

    self.grid_produto.grid_columnconfigure(0, weight=1)
    self.grid_produto.grid_columnconfigure(1, weight=1)

    self.label_titulo_prod = Label(
        self.grid_produto, 
        text="Criar ou Editar Produtos",
        font=("Helvetica", 16, "bold"),
        bg=Color.white.value
    )
    self.label_titulo_prod.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

    self.label_prod_nome = Label(self.grid_produto, text="Nome do Produto", bg=Color.white.value)
    self.label_prod_nome.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
    self.entry_prod_nome = Entry(self.grid_produto)
    self.entry_prod_nome.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

    self.label_quant_estoque = Label(self.grid_produto, text="Estoque Atual", bg=Color.white.value)
    self.label_quant_estoque.grid(row=3, column=0, sticky="w", padx=10)
    self.entry_quant_estoque = Entry(self.grid_produto)
    self.entry_quant_estoque.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

    self.label_min_estoque = Label(self.grid_produto, text="Estoque Mínimo", bg=Color.white.value)
    self.label_min_estoque.grid(row=3, column=1, sticky="w", padx=10)
    self.entry_min_estoque = Entry(self.grid_produto)
    self.entry_min_estoque.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

    self.label_valor_venda = Label(self.grid_produto, text="Valor de Venda", bg=Color.white.value)
    self.label_valor_venda.grid(row=5, column=0, sticky="w", padx=10)
    self.entry_valor_venda = Entry(self.grid_produto)
    self.entry_valor_venda.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")

    self.label_valor_custo = Label(self.grid_produto, text="Valor de Custo", bg=Color.white.value)
    self.label_valor_custo.grid(row=5, column=1, sticky="w", padx=10)
    self.entry_valor_custo = Entry(self.grid_produto)
    self.entry_valor_custo.grid(row=6, column=1, padx=10, pady=(0, 10), sticky="ew")

    # Botões
    self.btn_add_produto = self.create_button(self.grid_produto, "Adicionar", command_func=self.add_produto)
    self.btn_add_produto.grid(row=7, column=1, pady=(0, 10))

    self.btn_editar_produto = self.create_button(self.grid_produto, "Atualizar", command_func=self.carregar_produtos)
    self.btn_editar_produto.grid(row=7, column=0, pady=(0, 10))

    # Campo de pesquisa
    self.entry_pesquisa = Entry(self.grid_produto)
    self.entry_pesquisa.grid(row=8, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
    self.entry_pesquisa.bind("<KeyRelease>", self.pesquisar_produto)

    # Treeview
    self.tree_produtos = ttk.Treeview(
        self.grid_produto, 
        columns=("id", "nome", "quant", "min", "venda", "custo"), 
        show="headings"
    )
    self.tree_produtos.grid(row=9, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")
    self.grid_produto.grid_rowconfigure(9, weight=1)

    for col in ("id", "nome", "quant", "min", "venda", "custo"):
        self.tree_produtos.heading(col, text=col.upper())
        self.tree_produtos.column(col, width=100)

    self.tree_produtos.bind("<<TreeviewSelect>>", self.preencher_campos_produto)

    # Carregar produtos
    self.carregar_produtos()


  def pesquisar_produto(self, event=None):
    termo = self.entry_pesquisa.get().lower()

    for item in self.tree_produtos.get_children():
        self.tree_produtos.delete(item)

    produtos = self.banco_dados.get_produtos()

    for p in produtos:
        if termo in p[1].lower():  # p[1] é o nome
            self.tree_produtos.insert("", "end", values=p)

  def carregar_produtos(self):
    for item in self.tree_produtos.get_children():
        self.tree_produtos.delete(item)

    produtos = self.banco_dados.get_produtos()

    for p in produtos:
        self.tree_produtos.insert("", "end", values=p)

  def preencher_campos_produto(self, event):
    item = self.tree_produtos.selection()
    if item:
        valores = self.tree_produtos.item(item[0], "values")

        self.entry_prod_nome.delete(0, END)
        self.entry_prod_nome.insert(0, valores[1])

        self.entry_quant_estoque.delete(0, END)
        self.entry_quant_estoque.insert(0, valores[2])

        self.entry_min_estoque.delete(0, END)
        self.entry_min_estoque.insert(0, valores[3])

        self.entry_valor_venda.delete(0, END)
        self.entry_valor_venda.insert(0, valores[4])

        self.entry_valor_custo.delete(0, END)
        self.entry_valor_custo.insert(0, valores[5])

  def add_produto(self):
    nome = self.entry_prod_nome.get()
    quant = self.entry_quant_estoque.get()
    quant_min = self.entry_min_estoque.get()
    preco_venda = self.entry_valor_venda.get()
    preco_custo = self.entry_valor_custo.get()

    if not nome or not quant or not preco_venda:
      messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
      return

    try:
      # Converte os tipos
      quant = int(quant)
      quant_min = int(quant_min)
      preco_venda = float(preco_venda)
      preco_custo = float(preco_custo)
      # Chama a função do banco
      resultado = self.banco_dados.add_produto(nome, quant, quant_min, preco_venda, preco_custo)
      if resultado is None:
          self.carregar_produtos()
          messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
      else:
          messagebox.showwarning("Aviso", resultado)

    except ValueError:
      messagebox.showerror("Erro", "Preencha os campos numéricos corretamente.")

  def mostrar_lista_produtos(self):
    # Esconde os campos do formulário
    widgets = [
        self.label_titulo_prod,
        self.label_prod_nome, self.entry_prod_nome,
        self.label_quant_estoque, self.entry_quant_estoque,
        self.label_min_estoque, self.entry_min_estoque,
        self.label_valor_venda, self.entry_valor_venda,
        self.label_valor_custo, self.entry_valor_custo,
        self.btn_salvar
    ]

    for widget in widgets:
        widget.grid_remove()

    # Mostra a Treeview
    self.tree_produtos.grid(row=0, column=0, columnspan=2, rowspan=10, sticky="nsew", padx=10, pady=10)

    # Carrega os dados
    self.carregar_produtos()


  def create_button(self, frame, text, command_func):  
    btn = Button(frame, 
                 text=text,
                 font=("Helvetica", 12, "bold"),
                 anchor="w",
                 command=command_func,
                 height=2,
                 bg=Color.light_blue.value, 
                 fg=Color.white.value, 
                 borderwidth=0, 
                 highlightthickness= 0, 
                 relief="flat")
    btn.grid(sticky="ew", pady=10, padx=10)

    return btn
    

  def destroy_window(self):
    self.root.destroy()        # Destroi a janela do Tkinter

root = Tk()
Application(root)