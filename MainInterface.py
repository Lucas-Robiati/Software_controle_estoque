from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from DataBase import *
from Modules import *


class Application(Validate):
    def __init__(self, root: 'Tk'):
        self.root = root
        self.banco_dados = Database_conect()
        self.validate_command_float = self.root.register(self.validate_float)
        self.validate_command_int = self.root.register(self.validate_int)
        self.validate_command_cpf = self.root.register(self.validate_cpf_entry)
        self.window()
        root.mainloop()

    def window(self):
        """Configura a janela principal"""
        self.root.title("Controle de Estoque")
        self.root.configure(background=Color.white.value)
        self.root.geometry("950x520")
        self.root.minsize(width=950, height=520)
        self.root.resizable(True, True)
        self.root.protocol('WM_DELETE_WINDOW', self.destroy_window)
        self.frame_principal = Frame(self.root, background=Color.white.value)

        self.layout_sidebar()
        self.layout_header()
        self.show_vendas()

    def layout_sidebar(self):
        """Configura a barra lateral"""
        self.root.grid_rowconfigure(0, weight=1)
        self.sidebar = Frame(self.root, background=Color.light_blue.value, width=150)
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # Botões do sidebar (mantidos como estão)
        self.btn_produtos = self.create_button(self.sidebar, "Estoque", command_func=self.layout_produtos)
        self.btn_entrada = self.create_button(self.sidebar, "Entrada", command_func=self.show_entrada)
        self.btn_saida = self.create_button(self.sidebar, "Venda", command_func=self.show_vendas)
        self.btn_cliente = self.create_button(self.sidebar, "Clientes", command_func=self.show_clientes)

    def layout_header(self):
        """Configura o cabeçalho"""
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.frame_principal.grid(row=0, column=1, sticky="nsew")
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        # Cria frame header
        self.header = Frame(self.frame_principal, height=50, background=Color.aqua_blue.value)
        self.header.grid(row=0, column=0, sticky="ew")

        # Label do título no header
        label_titulo = Label(
            self.header,
            text="Sistema de Controle de Estoque",
            bg=Color.aqua_blue.value,
            fg="white",
            font=("Helvetica", 18, "bold")
        )
        label_titulo.pack(expand=True, fill="both")

    # ==============================================================
    # SEÇÃO DE PRODUTOS
    # ==============================================================
    def layout_produtos(self):
        """Mostra a interface de gerenciamento de produtos"""
        self.clear_main_content()
        self.grid_produto = Frame(self.frame_principal, background=Color.white.value)
        self.grid_produto.grid(row=1, column=0, sticky="nsew", padx=100, pady=75)
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.grid_produto.grid_columnconfigure(0, weight=1)
        self.grid_produto.grid_columnconfigure(1, weight=1)

        # Título
        Label(
            self.grid_produto,
            text="Criar ou Editar Produtos",
            font=("Helvetica", 16, "bold"),
            bg=Color.white.value
        ).grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        # Campos do formulário
        self.label_prod_nome = Label(self.grid_produto, text="Nome do Produto", bg=Color.white.value)
        self.label_prod_nome.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
        self.entry_prod_nome = Entry(self.grid_produto)
        self.entry_prod_nome.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="ew")

        self.label_quant_estoque = Label(self.grid_produto, text="Estoque Atual", bg=Color.white.value)
        self.label_quant_estoque.grid(row=3, column=0, sticky="w", padx=10)
        self.entry_quant_estoque = Entry(self.grid_produto, validate="key", validatecommand=(self.validate_command_int, "%P"))
        self.entry_quant_estoque.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.label_min_estoque = Label(self.grid_produto, text="Estoque Mínimo", bg=Color.white.value)
        self.label_min_estoque.grid(row=3, column=1, sticky="w", padx=10)
        self.entry_min_estoque = Entry(self.grid_produto, validate="key", validatecommand=(self.validate_command_int, "%P"))
        self.entry_min_estoque.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

        self.label_valor_venda = Label(self.grid_produto, text="Valor de Venda", bg=Color.white.value)
        self.label_valor_venda.grid(row=5, column=0, sticky="w", padx=10)
        self.entry_valor_venda = Entry(self.grid_produto, validate="key", validatecommand=(self.validate_command_float, "%P"))
        self.entry_valor_venda.grid(row=6, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.label_valor_custo = Label(self.grid_produto, text="Valor de Custo", bg=Color.white.value)
        self.label_valor_custo.grid(row=5, column=1, sticky="w", padx=10)
        self.entry_valor_custo = Entry(self.grid_produto, validate="key", validatecommand=(self.validate_command_float, "%P"))
        self.entry_valor_custo.grid(row=6, column=1, padx=10, pady=(0, 10), sticky="ew")

        # Botões (padronizados)
        frame_botoes = Frame(self.grid_produto, bg=Color.white.value)
        frame_botoes.grid(row=7, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        frame_botoes.grid_columnconfigure((0, 1, 2), weight=1)

        Button(
            frame_botoes, 
            text="Adicionar", 
            bg="#4CAF50", 
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.adicionar_produto
        ).grid(row=0, column=0, padx=5, sticky="ew")

        Button(
            frame_botoes, 
            text="Atualizar", 
            bg="#2196F3", 
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.atualizar_produto
        ).grid(row=0, column=1, padx=5, sticky="ew")

        Button(
            frame_botoes, 
            text="Deletar", 
            bg="#F44336", 
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.deletar_produto
        ).grid(row=0, column=2, padx=5, sticky="ew")

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

        scroll_produto = Scrollbar(self.grid_produto, orient="vertical", command=self.tree_produtos.yview)
        scroll_produto.grid(row=9, column=2, sticky="ns")
        self.tree_produtos.configure(yscrollcommand=scroll_produto.set)


        self.tree_produtos.bind("<<TreeviewSelect>>", self.preencher_campos_produto)
        self.carregar_produtos()

    def preencher_treeview(self, produtos):
        """Preenche a treeview com a lista de produtos"""
        self.tree_produtos.delete(*self.tree_produtos.get_children())

        # Configura a cor vermelha para produtos com estoque baixo
        self.tree_produtos.tag_configure("estoque_baixo", background="#ffe5e5")  # vermelho claro

        for p in produtos:
            id_, nome, quant, min_, venda, custo = p
            tag = "estoque_baixo" if int(quant) <= int(min_) else ""
            self.tree_produtos.insert("", "end", values=p, tags=(tag,))


    def pesquisar_produto(self, event=None):
        """Filtra produtos conforme texto digitado"""
        termo = self.entry_pesquisa.get().lower()
        produtos = self.banco_dados.get_produtos()
        filtrados = [p for p in produtos if termo in p[1].lower()]
        self.preencher_treeview(filtrados)

    def carregar_produtos(self):
        """Carrega todos os produtos na treeview"""
        produtos = self.banco_dados.get_produtos()
        self.preencher_treeview(produtos)

    def preencher_campos_produto(self, event):
        """Preenche os campos do formulário com o produto selecionado"""
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

    def adicionar_produto(self):
        """Adiciona um novo produto ao banco de dados"""
        nome = self.entry_prod_nome.get()
        quant = self.entry_quant_estoque.get()
        quant_min = self.entry_min_estoque.get()
        preco_venda = self.entry_valor_venda.get()
        preco_custo = self.entry_valor_custo.get()

        if not nome or not quant or not preco_venda:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return

        try:
            quant = int(quant)
            quant_min = int(quant_min)
            preco_venda = float(preco_venda)
            preco_custo = float(preco_custo)
            
            resultado = self.banco_dados.add_produto(nome, quant, quant_min, preco_venda, preco_custo)
            if resultado is None:
                self.carregar_produtos()
                messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            else:
                messagebox.showwarning("Aviso", resultado)

        except ValueError:
            messagebox.showerror("Erro", "Preencha os campos numéricos corretamente.")

    def atualizar_produto(self):
        """Atualiza um produto existente"""
        item = self.tree_produtos.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar.")
            return

        id_produto = int(self.tree_produtos.item(item[0], "values")[0])
        nome = self.entry_prod_nome.get()
        quant = self.entry_quant_estoque.get()
        quant_min = self.entry_min_estoque.get()
        preco_venda = self.entry_valor_venda.get()
        preco_custo = self.entry_valor_custo.get()

        if not nome or not preco_venda or not quant:
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
            return

        try:
            quant = int(quant)
            quant_min = int(quant_min)
            preco_venda = float(preco_venda)
            preco_custo = float(preco_custo)

            resultado = self.banco_dados.update_produto(
                id=id_produto,
                produto=None,
                new_nome=nome,
                new_preco_un=preco_venda,
                new_quant=quant,
                new_estoque_min=quant_min,
                new_preco_cus=preco_custo
            )

            if resultado is None:
                self.carregar_produtos()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            else:
                messagebox.showwarning("Aviso", resultado)

        except ValueError:
            messagebox.showerror("Erro", "Preencha os campos numéricos corretamente.")

    def deletar_produto(self):
        """Remove um produto do banco de dados"""
        item = self.tree_produtos.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um produto para deletar.")
            return

        confirmar = messagebox.askyesno("Confirmar", "Tem certeza que deseja deletar este produto?")
        if not confirmar:
            return

        id_produto = int(self.tree_produtos.item(item[0], "values")[0])
        resultado = self.banco_dados.remove_produto(id=id_produto)

        if resultado is None:
            self.carregar_produtos()
            messagebox.showinfo("Sucesso", "Produto deletado com sucesso.")
        else:
            messagebox.showwarning("Aviso", resultado)

    # ==============================================================
    # SEÇÃO DE ENTRADAS
    # ==============================================================
    def show_entrada(self):
        """Mostra a interface de registro de entradas no estoque"""
        self.clear_main_content()
        self.init_layout_entrada()
        self.init_componentes_entrada()
        self.carregar_produtos_entrada()
        self.produtos_na_entrada = []

    def init_layout_entrada(self):
        """Configura o layout da tela de entradas"""
        self.grid_entrada = Frame(self.frame_principal, background=Color.white.value)
        self.grid_entrada.grid(row=1, column=0, sticky="nsew", padx=100, pady=75)
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.grid_entrada.grid_columnconfigure(0, weight=1)

        Label(
            self.grid_entrada,
            text="Registro de Entrada no Estoque",
            font=("Helvetica", 16, "bold"),
            bg=Color.white.value
        ).grid(row=0, column=0, pady=(10, 20), sticky="n")

    def init_componentes_entrada(self):
        """Configura os componentes da tela de entradas"""
        self.produto_var_entrada = StringVar()
        Label(
            self.grid_entrada,
            text="Produto",
            bg=Color.white.value
        ).grid(row=1, column=0, sticky="w", padx=(0, 5), pady=(0, 2))

        self.combo_entrada_produto = ttk.Combobox(self.grid_entrada, textvariable=self.produto_var_entrada)
        self.combo_entrada_produto.grid(row=2, column=0, padx=(0, 5), pady=(0, 10), sticky="ew")
        self.grid_entrada.grid_columnconfigure(0, weight=1)

        self.combo_entrada_produto.bind('<KeyRelease>', self.filtrar_produtos_entrada)
        self.combo_entrada_produto.bind("<Tab>", lambda e: (self.combo_entrada_produto.event_generate('<Down>'), "break"))

        self.e_entrada_quant = self.create_label_entry(self.grid_entrada, "Quantidade", row=3, col=0, validate_command=self.validate_command_int)

        # Label para mensagens de erro/sucesso
        self.label_msg_entrada = Label(
            self.grid_entrada,
            text="",
            fg="red",
            bg=Color.white.value,
            font=("Arial", 10, "italic")
        )
        self.label_msg_entrada.grid(row=4, column=0, sticky="w", pady=(5, 5), padx=5)
        self.label_msg_entrada.grid_remove()

        # Botões (padronizados)
        frame_botoes = Frame(self.grid_entrada, bg=Color.white.value)
        frame_botoes.grid(row=5, column=0, pady=(10, 20), sticky="ew")
        frame_botoes.grid_columnconfigure((0, 1, 2), weight=1)

        Button(
            frame_botoes,
            text="Adicionar/Atualizar Produto",
            bg="#4CAF50",
            fg="white",
            command=self.adicionar_ou_atualizar_produto_entrada,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=5, sticky="ew")

        Button(
            frame_botoes,
            text="Remover Produto",
            bg="#F44336",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.remover_produto_entrada
        ).grid(row=0, column=1, padx=5, sticky="ew")

        Button(
            frame_botoes,
            text="Salvar Entrada",
            bg="#2196F3",
            fg="white",
            command=self.salvar_entrada,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, padx=5, sticky="ew")

        # Treeview
        cols = ("produto", "quantidade")
        self.tree_entrada = ttk.Treeview(self.grid_entrada, columns=cols, show="headings")
        self.tree_entrada.grid(row=6, column=0, sticky="nsew", padx=10, pady=(10, 10))
        self.grid_entrada.grid_rowconfigure(6, weight=1)

        for col in cols:
            self.tree_entrada.heading(col, text=col.upper())
            self.tree_entrada.column(col, width=150, anchor="center")

        scroll_entrada = Scrollbar(self.grid_entrada, orient="vertical", command=self.tree_entrada.yview)
        scroll_entrada.grid(row=6, column=1, sticky="ns")
        self.tree_entrada.configure(yscrollcommand=scroll_entrada.set)

        self.tree_entrada.bind("<<TreeviewSelect>>", self.selecionar_produto_entrada)

    def mostrar_erro_entrada(self, msg):
        if msg:
            self.label_msg_entrada.config(text=msg)
            self.label_msg_entrada.grid()
        else:
            self.label_msg_entrada.grid_remove()

    def adicionar_ou_atualizar_produto_entrada(self):
        produto = self.combo_entrada_produto.get().strip()
        quant = self.e_entrada_quant.get().strip()

        if not produto or not quant:
            return self.mostrar_erro_entrada("Produto e quantidade são obrigatórios.")

        try:
            quant_int = int(quant)
            if quant_int <= 0:
                raise ValueError
        except ValueError:
            return self.mostrar_erro_entrada("Quantidade deve ser um número inteiro positivo.")

        # Atualiza ou adiciona na lista produtos_na_entrada
        ja_existe = False
        for p in self.produtos_na_entrada:
            if produto in p:
                p[produto] = quant_int
                ja_existe = True
                break
        if not ja_existe:
            self.produtos_na_entrada.append({produto: quant_int})

        # Atualizar Treeview
        for item in self.tree_entrada.get_children():
            if self.tree_entrada.item(item)["values"][0] == produto:
                self.tree_entrada.item(item, values=(produto, quant_int))
                break
        else:
            self.tree_entrada.insert("", "end", values=(produto, quant_int))

        # Limpar campos e mensagem
        self.combo_entrada_produto.set("")
        self.e_entrada_quant.delete(0, END)
        self.mostrar_erro_entrada("")

    def selecionar_produto_entrada(self, event):
        item = self.tree_entrada.selection()
        if item:
            valores = self.tree_entrada.item(item[0], "values")
            produto, quantidade = valores
            self.combo_entrada_produto.set(produto)
            self.e_entrada_quant.delete(0, END)
            self.e_entrada_quant.insert(0, quantidade)
            self.mostrar_erro_entrada("")

    def remover_produto_entrada(self):
        item = self.tree_entrada.selection()
        if not item:
            self.mostrar_erro_entrada("Selecione um produto para remover.")
            return

        produto = self.tree_entrada.item(item[0], "values")[0]
        self.produtos_na_entrada = [p for p in self.produtos_na_entrada if produto not in p]
        self.tree_entrada.delete(item[0])

        self.combo_entrada_produto.set("")
        self.e_entrada_quant.delete(0, END)
        self.mostrar_erro_entrada("")


    def salvar_entrada(self):
        """Salva a entrada de produtos no banco de dados"""
        if not self.produtos_na_entrada:
            return messagebox.showerror("Erro", "Adicione pelo menos um produto à entrada.")

        produtos_dict = {}
        for p in self.produtos_na_entrada:
            for k, v in p.items():
                produtos_dict[k] = produtos_dict.get(k, 0) + v

        for produto, quant in produtos_dict.items():
            erro = self.banco_dados.aumentar_estoque(produto=produto, quant_aumentar=quant)
            if erro:
                messagebox.showerror("Erro", erro)
                return

        messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")
        self.produtos_na_entrada.clear()
        self.tree_entrada.delete(*self.tree_entrada.get_children())

    def carregar_produtos_entrada(self):
        """Carrega a lista de produtos para o combobox"""
        produtos = [p[1] for p in self.banco_dados.get_produtos()]
        self.combo_entrada_produto['values'] = produtos
        self.combo_entrada_produto._values_backup = produtos

    def filtrar_produtos_entrada(self, event):
        """Filtra os produtos no combobox conforme texto digitado"""
        texto = self.produto_var_entrada.get().lower()
        produtos_filtrados = [p for p in self.combo_entrada_produto._values_backup if texto in p.lower()]
        self.combo_entrada_produto['values'] = produtos_filtrados

    # ==============================================================
    # SEÇÃO DE VENDAS
    # ==============================================================
    def show_vendas(self):
        """Mostra a interface de registro de vendas"""
        self.clear_main_content()
        self.init_layout_vendas()
        self.init_componentes_vendas()
        self.carregar_produtos_vendas()
        self.produtos_na_venda = []

    def init_layout_vendas(self):
        """Configura o layout da tela de vendas"""
        self.grid_vendas = Frame(self.frame_principal, background=Color.white.value)
        self.grid_vendas.grid(row=1, column=0, sticky="nsew", padx=100, pady=75)
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.grid_vendas.grid_columnconfigure(0, weight=1)

        Label(
            self.grid_vendas,
            text="Registro de Vendas",
            font=("Helvetica", 16, "bold"),
            bg=Color.white.value
        ).grid(row=0, column=0, pady=(10, 20), sticky="n")

    def init_componentes_vendas(self):
        """Configura os componentes da tela de vendas"""
        self.e_venda_cpf = self.create_label_entry(self.grid_vendas, "CPF do Cliente", row=1, col=0)
        self.e_venda_cpf.config(validate="key", validatecommand=(self.validate_command_cpf, "%S", "%i", "%P"))

        self.produto_var = StringVar()
        Label(
            self.grid_vendas,
            text="Produto",
            bg=Color.white.value
        ).grid(row=3, column=0, sticky="w", padx=(0, 5), pady=(0, 2))

        self.combo_venda_produto = ttk.Combobox(self.grid_vendas, textvariable=self.produto_var)
        self.combo_venda_produto.grid(row=4, column=0, padx=(0, 5), pady=(0, 10), sticky="ew")
        self.grid_vendas.grid_columnconfigure(0, weight=1)

        self.combo_venda_produto.bind('<KeyRelease>', self.filtrar_produtos)
        self.combo_venda_produto.bind("<Tab>", lambda e: (self.combo_venda_produto.event_generate('<Down>'), "break"))

        self.e_venda_quant = self.create_label_entry(self.grid_vendas, "Quantidade", row=5, col=0, validate_command=self.validate_command_int)

        # Label para mostrar mensagens
        self.label_msg_venda = Label(
            self.grid_vendas,
            text="",
            fg="red",
            bg=Color.white.value,
            font=("Arial", 10, "italic")
        )
        self.label_msg_venda.grid(row=6, column=0, sticky="w", pady=(5, 5), padx=5)
        self.label_msg_venda.grid_remove()  # Oculta o label inicialmente

        # Botões
        frame_botoes = Frame(self.grid_vendas, bg=Color.white.value)
        frame_botoes.grid(row=7, column=0, pady=(10, 5), sticky="ew")
        frame_botoes.grid_columnconfigure((0, 1), weight=1)

        Button(
            frame_botoes,
            text="Adicionar/Atualizar Produto",
            bg="#4CAF50",
            fg="white",
            command=self.adicionar_produto_venda,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=5, sticky="ew")

        Button(
            frame_botoes,
            text="Salvar Venda",
            bg="#2196F3",
            fg="white",
            command=self.salvar_venda,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, padx=5, sticky="ew")

        # Treeview
        cols = ("produto", "quantidade", "preco_unit", "preco_total")
        self.tree_venda = ttk.Treeview(self.grid_vendas, columns=cols, show="headings")
        self.tree_venda.grid(row=8, column=0, sticky="nsew", padx=10, pady=(5, 0))
        self.grid_vendas.grid_rowconfigure(8, weight=1)

        self.tree_venda.heading("produto", text="PRODUTO")
        self.tree_venda.heading("quantidade", text="QUANT.")
        self.tree_venda.heading("preco_unit", text="VALOR UNIT.")
        self.tree_venda.heading("preco_total", text="VALOR TOTAL")

        for col in cols:
            self.tree_venda.column(col, width=120, anchor="center")

        self.tree_venda.bind("<<TreeviewSelect>>", self.selecionar_produto_venda)

        # Scrollbar
        scroll_venda = Scrollbar(self.grid_vendas, orient="vertical", command=self.tree_venda.yview)
        scroll_venda.grid(row=8, column=1, sticky="ns")
        self.tree_venda.configure(yscrollcommand=scroll_venda.set)

        self.label_total_venda = Label(
            self.grid_vendas,
            text="Total da Venda: R$ 0.00",
            font=("Arial", 12, "bold"),
            bg=Color.white.value,
            anchor="e"
        )
        self.label_total_venda.grid(row=10, column=0, sticky="e", padx=10, pady=(0, 10))

        # Botão remover
        Button(
            self.grid_vendas,
            text="Remover Produto Selecionado",
            bg="#F44336",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.remover_produto_venda
        ).grid(row=9, column=0, pady=(10, 10), sticky="ew", padx=10)

    def mostrar_erro_venda(self, msg):
        if msg:
            self.label_msg_venda.config(text=msg)
            self.label_msg_venda.grid()  # Mostra o label
        else:
            self.label_msg_venda.grid_remove()  # Oculta o label se não há erro

    def selecionar_produto_venda(self, event):
        item = self.tree_venda.selection()
        if item:
            valores = self.tree_venda.item(item[0], "values")
            produto = valores[0]
            quantidade = valores[1]

            self.combo_venda_produto.set(produto)
            self.e_venda_quant.delete(0, END)
            self.e_venda_quant.insert(0, quantidade)

    def remover_produto_venda(self):
        item = self.tree_venda.selection()
        if not item:
            self.mostrar_erro_venda("Selecione um produto para remover.")
            return

        produto = self.tree_venda.item(item[0], "values")[0]
        self.produtos_na_venda = [p for p in self.produtos_na_venda if produto not in p]
        self.tree_venda.delete(item[0])
        self.combo_venda_produto.set("")
        self.e_venda_quant.delete(0, END)
        self.mostrar_erro_venda("")
        self.atualizar_total_venda()

    def carregar_produtos_vendas(self):
        """Carrega a lista de produtos para o combobox"""
        produtos = [p[1] for p in self.banco_dados.get_produtos()]
        self.combo_venda_produto['values'] = produtos
        self.combo_venda_produto._values_backup = produtos

    def filtrar_produtos(self, event):
        """Filtra os produtos no combobox conforme texto digitado"""
        texto = self.produto_var.get().lower()
        produtos_filtrados = [p for p in self.combo_venda_produto._values_backup if texto in p.lower()]
        self.combo_venda_produto['values'] = produtos_filtrados

    def adicionar_produto_venda(self):
        """Adiciona ou atualiza um produto na venda"""
        produto = self.combo_venda_produto.get().strip()
        quant = self.e_venda_quant.get().strip()

        if not produto or not quant:
            return self.mostrar_erro_venda("Produto e quantidade são obrigatórios.")

        try:
            quant_int = int(quant)
            if quant_int <= 0:
                raise ValueError
        except ValueError:
            return self.mostrar_erro_venda("Quantidade deve ser um número inteiro positivo.")

        # Buscar preço unitário do produto
        try:
            self.banco_dados.get_db_connection()
            self.banco_dados.execute_query("SELECT preco_un FROM produto WHERE nome = %s", (produto,))
            preco_unit = self.banco_dados.cur.fetchone()
            if preco_unit is None:
                return self.mostrar_erro_venda("Produto não encontrado.")
            preco_unit = float(preco_unit[0])
        except Exception as e:
            return self.mostrar_erro_venda(f"Erro ao buscar preço: {e}")

        preco_total = preco_unit * quant_int

        # Atualizar lista
        ja_existe = False
        for p in self.produtos_na_venda:
            if produto in p:
                p[produto] = quant_int
                ja_existe = True
                break
        if not ja_existe:
            self.produtos_na_venda.append({produto: quant_int})

        # Atualizar Treeview
        for item in self.tree_venda.get_children():
            if self.tree_venda.item(item)["values"][0] == produto:
                self.tree_venda.item(item, values=(produto, quant_int, f"R$ {preco_unit:.2f}", f"R$ {preco_total:.2f}"))
                break
        else:
            self.tree_venda.insert("", "end", values=(produto, quant_int, f"R$ {preco_unit:.2f}", f"R$ {preco_total:.2f}"))

        # Limpar campos
        self.combo_venda_produto.set("")
        self.e_venda_quant.delete(0, END)
        self.mostrar_erro_venda("")
        self.atualizar_total_venda()

    def atualizar_total_venda(self):
        """Atualiza o valor total da venda"""
        total = 0.0
        for item in self.tree_venda.get_children():
            valor_total = self.tree_venda.item(item, "values")[3]
            valor = float(valor_total.replace("R$", "").replace(",", "."))
            total += valor
        self.label_total_venda.config(text=f"Total da Venda: R$ {total:.2f}")

    def salvar_venda(self):
        """Salva a venda no banco de dados"""
        cpf = self.e_venda_cpf.get().strip()

        if not cpf:
            return messagebox.showerror("Erro", "CPF do cliente é obrigatório.")

        # Verifica se o cliente está cadastrado
        if not self.banco_dados.cliente_existe(cpf):
            return messagebox.showerror("Erro", f"Cliente com CPF {cpf} não está cadastrado.")

        if not self.produtos_na_venda:
            return messagebox.showerror("Erro", "Adicione pelo menos um produto à venda.")

        produtos_dict = {}
        for p in self.produtos_na_venda:
            for k, v in p.items():
                produtos_dict[k] = produtos_dict.get(k, 0) + v

        erro = self.banco_dados.new_venda(produtos_dict, cpf)
        if erro:
            messagebox.showerror("Erro", erro)
        else:
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            self.produtos_na_venda.clear()
            self.tree_venda.delete(*self.tree_venda.get_children())
            self.e_venda_cpf.delete(0, END)
            self.label_total_venda.config(text="Total da Venda: R$ 0.00")



    # ==============================================================
    # SEÇÃO DE CLIENTES
    # ==============================================================
    def show_clientes(self):
        """Mostra a interface de gerenciamento de clientes"""
        self.clear_main_content()
        self.init_layout_clientes()
        self.init_componentes_clientes()
        self.carregar_clientes()

    def init_layout_clientes(self):
        """Configura o layout da tela de clientes"""
        self.grid_clientes = Frame(self.frame_principal, background=Color.white.value)
        self.grid_clientes.grid(row=1, column=0, sticky="nsew", padx=100, pady=75)
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.grid_clientes.grid_columnconfigure(0, weight=1)
        self.grid_clientes.grid_columnconfigure(1, weight=1)

        Label(
            self.grid_clientes,
            text="Cadastro de Clientes",
            font=("Helvetica", 16, "bold"),
            bg=Color.white.value
        ).grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

    def init_componentes_clientes(self):
        """Configura os componentes da tela de clientes"""
        self.e_cli_nome = self.create_label_entry(self.grid_clientes, "Nome", row=1, col=0, col_span=2)
        self.e_cli_tel = self.create_label_entry(self.grid_clientes, "Telefone", row=3, col=0)
        self.e_cli_email = self.create_label_entry(self.grid_clientes, "Email", row=3, col=1)
        self.e_cli_cpf = self.create_label_entry(self.grid_clientes, "CPF", row=5, col=0)
        self.e_cli_cpf.config(validate="key", validatecommand=(self.validate_command_cpf, "%S", "%i", "%P"))
        self.e_cli_cep = self.create_label_entry(self.grid_clientes, "CEP", row=5, col=1)

        self._editar_cpf_ref = None  # guarda CPF original durante edição

        # Botões (padronizados)
        frame_botoes = Frame(self.grid_clientes, bg=Color.white.value)
        frame_botoes.grid(row=7, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        frame_botoes.grid_columnconfigure((0, 1, 2), weight=1)

        Button(
            frame_botoes,
            text="Editar",
            bg="#FFA500",
            fg="white",
            command=self.preparar_edicao_cliente,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=5, sticky="ew")

        Button(
            frame_botoes,
            text="Salvar",
            bg="#4CAF50",
            fg="white",
            command=self.salvar_cliente,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=1, padx=5, sticky="ew")

        Button(
            frame_botoes,
            text="Excluir",
            bg="#F44336",
            fg="white",
            command=self.excluir_cliente,
            font=("Arial", 12, "bold")
        ).grid(row=0, column=2, padx=5, sticky="ew")

        # Campo de pesquisa por CPF
        busca_frame = Frame(self.grid_clientes, bg=Color.white.value)
        busca_frame.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")
        Label(busca_frame, text="CPF:", bg=Color.white.value).pack(side=LEFT)
        self.busca_entry = Entry(busca_frame)
        self.busca_entry.pack(side=LEFT, padx=5)

        Button(
            busca_frame,
            text="Buscar/Editar",
            command=self.buscar_por_cpf,
            bg="#2196F3",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side=LEFT, padx=5)

        Button(
            busca_frame,
            text="Excluir por CPF",
            command=self.excluir_por_cpf,
            bg="#F44336",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side=LEFT, padx=5)

        # Treeview de clientes
        self.tree_cli = ttk.Treeview(
            self.grid_clientes,
            columns=("nome", "telefone", "email", "cpf", "cep"),
            show="headings"
        )
        self.tree_cli.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 10))
        self.grid_clientes.grid_rowconfigure(8, weight=1)

        for col in ("nome", "telefone", "email", "cpf", "cep"):
            self.tree_cli.heading(col, text=col.upper())
            self.tree_cli.column(col, width=100, anchor="center")

        scroll_cli = Scrollbar(self.grid_clientes, orient="vertical", command=self.tree_cli.yview)
        scroll_cli.grid(row=9, column=2, sticky="ns")
        self.tree_cli.configure(yscrollcommand=scroll_cli.set)

    def preparar_edicao_cliente(self):
        """Prepara os campos para edição de um cliente"""
        item = self.tree_cli.focus()
        if not item:
            return messagebox.showwarning("Aviso", "Selecione um cliente.")
        
        valores = self.tree_cli.item(item, "values")
        self._editar_cpf_ref = valores[3]
        
        self.e_cli_nome.delete(0, END)
        self.e_cli_nome.insert(0, valores[0])
        
        self.e_cli_tel.delete(0, END)
        self.e_cli_tel.insert(0, valores[1])
        
        self.e_cli_email.delete(0, END)
        self.e_cli_email.insert(0, valores[2])
        
        self.e_cli_cpf.delete(0, END)
        self.e_cli_cpf.insert(0, valores[3])

        self.e_cli_cep.delete(0, END)
        self.e_cli_cep.insert(0,valores[4])
  
    def salvar_cliente(self):
        nome  = self.e_cli_nome.get().strip()
        tel   = self.e_cli_tel.get().strip()
        email = self.e_cli_email.get().strip()
        cpf   = self.e_cli_cpf.get().strip()
        cep   = self.e_cli_cep.get().strip()

        # ----------- Validações
        if not all((nome, tel, email, cpf, cep)):
            return messagebox.showerror("Erro", "Todos os campos são obrigatórios.")

        if not re.fullmatch(r"[A-Za-zÀ-ÿ\s]+", nome):
            return messagebox.showerror("Erro", "Nome não pode conter números ou caracteres especiais.")

        if not re.fullmatch(r"\d{10,11}", tel):
            return messagebox.showerror("Erro", "Telefone deve conter 10 ou 11 dígitos numéricos.")

        if not re.fullmatch(r"[\w\.-]+@[\w\.-]+\.\w{2,}", email):
            return messagebox.showerror("Erro", "Email inválido. Ex.: usuario@gmail.com")

        if not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf):
            return messagebox.showerror("Erro", "CPF deve estar no formato 000.000.000-00")
        
        if not re.fullmatch(r"\d{5}-\d{3}", cep):
            return messagebox.showerror("Erro", "CEP deve estar no formato 00000-000")


        # ----------- Chamada ao banco ---------------
        if self._editar_cpf_ref:
            erro = self.banco_dados.update_usuario(
                cpf=self._editar_cpf_ref,
                new_name=nome, new_telefone=tel,
                new_email=email, new_cpf=cpf, new_cep=cep
            )
        else:
            erro = self.banco_dados.add_pessoa(nome, tel, email, cpf, cep)

        if erro:
            return messagebox.showerror("Erro", erro)

        msg = "atualizado" if self._editar_cpf_ref else "adicionado"
        messagebox.showinfo("Sucesso", f"Cliente {msg} com sucesso! 🎉")

        self._editar_cpf_ref = None
        self.show_clientes()

    def excluir_cliente(self):
        """Remove um cliente do banco de dados"""
        item = self.tree_cli.focus()
        if not item:
            return messagebox.showwarning("Aviso", "Selecione um cliente.")
            
        valores = self.tree_cli.item(item, "values")
        if messagebox.askyesno("Confirmar", f"Excluir CPF {valores[3]}?"):
            erro = self.banco_dados.remove_usuario(valores[3])
            if erro:
                messagebox.showerror("Erro", erro)
            else:
                messagebox.showinfo("Sucesso", "Cliente excluído!")
                self.carregar_clientes()

    def buscar_por_cpf(self):
        """Busca um cliente pelo CPF e preenche os campos"""
        cpf = self.busca_entry.get().strip()
        for cli in self.banco_dados.listar_clientes():
            if cli[3] == cpf:
                self._editar_cpf_ref = cli[3]
                self.e_cli_nome.delete(0, END)
                self.e_cli_nome.insert(0, cli[0])
                self.e_cli_tel.delete(0, END)
                self.e_cli_tel.insert(0, cli[1])
                self.e_cli_email.delete(0, END)
                self.e_cli_email.insert(0, cli[2])
                self.e_cli_cpf.delete(0, END)
                self.e_cli_cpf.insert(0, cli[3])
                self.e_cli_cep.delete(0, END)
                self.e_cli_cep.insert(0, cli[4])
                return messagebox.showinfo("Sucesso", "Cliente encontrado!")
        
        messagebox.showinfo("Info", "Cliente não encontrado.")

    def excluir_por_cpf(self):
        """Remove um cliente pelo CPF"""
        cpf = self.busca_entry.get().strip()
        if not cpf:
            return messagebox.showwarning("Aviso", "Digite um CPF.")
            
        if messagebox.askyesno("Confirmar", f"Excluir CPF {cpf}?"):
            erro = self.banco_dados.remove_usuario(cpf)
            if erro:
                messagebox.showerror("Erro", erro)
            else:
                messagebox.showinfo("Sucesso", "Cliente excluído!")
                self.carregar_clientes()

    def carregar_clientes(self):
        """Carrega todos os clientes na treeview"""
        self.tree_cli.delete(*self.tree_cli.get_children())
        for cli in self.banco_dados.listar_clientes():
            self.tree_cli.insert("", "end", values=cli)

    # ==============================================================
    # MÉTODOS AUXILIARES
    # ==============================================================
    def create_button(self, frame, text, command_func):
        """Cria um botão padronizado para o sidebar"""
        btn = Button(
            frame,
            text=text,
            font=("Helvetica", 12, "bold"),
            anchor="w",
            command=command_func,
            height=2,
            bg=Color.light_blue.value,
            fg=Color.white.value,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        btn.grid(sticky="ew", pady=10, padx=10)
        return btn

    def create_label_entry(self, parent, text, row, col, col_span=1, validate_command=None):
        """Cria um par label/entry padronizado"""
        Label(parent, text=text, bg=Color.white.value).grid(
            row=row, column=col, columnspan=col_span, sticky="w", padx=(0, 5), pady=(0, 2)
        )
        entry = Entry(parent, validate="key", validatecommand=(validate_command, "%P"))
        entry.grid(row=row+1, column=col, columnspan=col_span, padx=(0, 5), pady=(0, 10), sticky="ew")
        return entry

    def clear_main_content(self):
        """Remove todos os widgets (exceto header) da área de conteúdo"""
        for widget in self.frame_principal.winfo_children():
            info = widget.grid_info()
            if info and int(info.get("row", 0)) >= 1:
                widget.destroy()

    def destroy_window(self):
        """Fecha a janela principal"""
        self.root.destroy()


root = Tk()
Application(root)
