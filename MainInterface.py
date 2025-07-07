from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from Modules import *

class Application(Validate):
  def __init__(self, root:'Tk'):
    self.root = root                               
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

    self.btn_produtos = self.create_button(self.sidebar, "Produtos", command=self.layout_produtos)
    self.btn_entrada = self.create_button(self.sidebar, "Entradas", command=None)
    self.btn_saida = self.create_button(self.sidebar, "Saidas", command=None)
    self.btn_cliente = self.create_button(self.sidebar, "Clientes", command=None)
    
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

  def create_button(self, frame, text, command):  
    btn = Button(frame, 
                 text=text,
                 font=("Helvetica", 12, "bold"),
                 anchor="w",
                 command=command,
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