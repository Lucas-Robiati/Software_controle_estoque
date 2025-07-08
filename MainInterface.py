from tkinter import *
from tkinter import ttk, messagebox

from DataBase import *
from Modules  import *


class Application(Validate):
    def __init__(self, root: "Tk"):
        self.root = root
        self.banco_dados = Database_conect()
        self.window()
        root.mainloop()

    def window(self):
        self.root.title("Controle de Estoque")
        self.root.configure(background=Color.white.value)
        self.root.geometry("950x520")
        self.root.minsize(width=950, height=520)
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.destroy_window)

        # Frame que abriga o cabeçalho + conteúdos centrais
        self.frame_principal = Frame(self.root, background=Color.white.value)
        self.frame_principal.grid(row=0, column=1, sticky="nsew")

        # Sidebar fixo
        self.layout_sidebar()
        # Cabeçalho fixo
        self.layout_header()
        # Tela inicial: Produtos
        self.layout_produtos()


    def layout_sidebar(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.sidebar = Frame(self.root, background=Color.light_blue.value, width=150)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_propagate(False)

        self.btn_produtos = self._create_sidebar_button("Produtos",  self.layout_produtos)
        self.btn_entrada  = self._create_sidebar_button("Entradas",  lambda: messagebox.showinfo("WIP", "Tela ainda não implementada"))
        self.btn_saida    = self._create_sidebar_button("Saídas",    lambda: messagebox.showinfo("WIP", "Tela ainda não implementada"))
        self.btn_cliente  = self._create_sidebar_button("Clientes",  self._show_clientes)

    def _create_sidebar_button(self, text, command):
        btn = Button(self.sidebar,
                     text=text,
                     font=("Helvetica", 12, "bold"),
                     anchor="w",
                     command=command,
                     height=2,
                     bg=Color.light_blue.value,
                     fg=Color.white.value,
                     borderwidth=0,
                     highlightthickness=0,
                     relief="flat")
        btn.grid(sticky="ew", pady=10, padx=10)
        return btn

    def layout_header(self):
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        self.header = Frame(self.frame_principal, height=50, background=Color.aqua_blue.value)
        self.header.grid(row=0, column=0, sticky="ew")
        Label(self.header, text="Sistema de Controle", bg=Color.aqua_blue.value,
              fg=Color.white.value, font=("Helvetica", 14, "bold")).pack(side=LEFT, padx=20)


    def layout_produtos(self):
        self.clear_main_content()

        self.grid_produto = Frame(self.frame_principal, background=Color.white.value)
        self.grid_produto.grid(row=1, column=0, sticky="nsew", padx=100, pady=75)
        self.frame_principal.grid_rowconfigure(1, weight=1)

        self.grid_produto.grid_columnconfigure((0, 1), weight=1)

        self.label_titulo_prod = Label(self.grid_produto, text="Criar ou Editar Produtos",
                                       font=("Helvetica", 16, "bold"), bg=Color.white.value)
        self.label_titulo_prod.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="n")

        # --- Campos
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

        # --- Botões (Adicionar / Atualizar / Remover)
        frame_botoes = Frame(self.grid_produto, bg=Color.white.value)
        frame_botoes.grid(row=7, column=0, columnspan=2, pady=(0, 10), sticky="ew")
        frame_botoes.grid_columnconfigure((0, 1, 2), weight=1)

        Button(frame_botoes, text="Adicionar",  command=self.add_produto).grid(row=0, column=0, padx=5, sticky="ew")
        Button(frame_botoes, text="Atualizar",  command=self.editar_produto).grid(row=0, column=1, padx=5, sticky="ew")
        Button(frame_botoes, text="Deletar",    command=self.deletar_produto).grid(row=0, column=2, padx=5, sticky="ew")

        # --- Busca
        self.entry_pesquisa = Entry(self.grid_produto)
        self.entry_pesquisa.grid(row=8, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="ew")
        self.entry_pesquisa.bind("<KeyRelease>", self.pesquisar_produto)

        # --- Treeview
        self.tree_produtos = ttk.Treeview(self.grid_produto,
                                          columns=("id", "nome", "quant", "min", "venda", "custo"),
                                          show="headings")
        self.tree_produtos.grid(row=9, column=0, columnspan=2, padx=10, pady=(5, 10), sticky="nsew")
        self.grid_produto.grid_rowconfigure(9, weight=1)

        for col in ("id", "nome", "quant", "min", "venda", "custo"):
            self.tree_produtos.heading(col, text=col.upper())
            self.tree_produtos.column(col, width=100)

        self.tree_produtos.bind("<<TreeviewSelect>>", self.preencher_campos_produto)

        self.carregar_produtos()


    def preencher_treeview(self, produtos):
        self.tree_produtos.delete(*self.tree_produtos.get_children())
        for p in produtos:
            self.tree_produtos.insert("", "end", values=p)

    def pesquisar_produto(self, _):
        termo = self.entry_pesquisa.get().lower()
        produtos = self.banco_dados.get_produtos()
        filtrados = [p for p in produtos if termo in p[1].lower()]
        self.preencher_treeview(filtrados)

    def carregar_produtos(self):
        self.preencher_treeview(self.banco_dados.get_produtos())

    def preencher_campos_produto(self, _):
        item = self.tree_produtos.selection()
        if item:
            valores = self.tree_produtos.item(item[0], "values")
            widgets = [self.entry_prod_nome, self.entry_quant_estoque, self.entry_min_estoque,
                       self.entry_valor_venda, self.entry_valor_custo]
            for w, v in zip(widgets, valores[1:]):
                w.delete(0, END)
                w.insert(0, v)

    def add_produto(self):
        nome         = self.entry_prod_nome.get()
        quant        = self.entry_quant_estoque.get()
        quant_min    = self.entry_min_estoque.get()
        preco_venda  = self.entry_valor_venda.get()
        preco_custo  = self.entry_valor_custo.get()

        if not (nome and quant and preco_venda):
            return messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios.")
        try:
            resultado = self.banco_dados.add_produto(nome, int(quant), int(quant_min or 0),
                                                     float(preco_venda), float(preco_custo or 0))
            if resultado:
                messagebox.showwarning("Aviso", resultado)
            else:
                self.carregar_produtos()
                messagebox.showinfo("Sucesso", "Produto cadastrado!")
        except ValueError:
            messagebox.showerror("Erro", "Preencha os campos numéricos corretamente.")

    def editar_produto(self):
        sel = self.tree_produtos.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione um produto.")
        valores = self.tree_produtos.item(sel[0], "values")
        try:
            resultado = self.banco_dados.update_produto(
                id=int(valores[0]),
                produto=None,
                new_nome=self.entry_prod_nome.get(),
                new_preco_un=float(self.entry_valor_venda.get()),
                new_quant=int(self.entry_quant_estoque.get()),
                new_estoque_min=int(self.entry_min_estoque.get() or 0),
                new_preco_cus=float(self.entry_valor_custo.get() or 0)
            )
            if resultado:
                messagebox.showwarning("Aviso", resultado)
            else:
                self.carregar_produtos()
                messagebox.showinfo("Sucesso", "Produto atualizado!")
        except ValueError:
            messagebox.showerror("Erro", "Preencha os campos numéricos corretamente.")

    def deletar_produto(self):
        sel = self.tree_produtos.selection()
        if not sel:
            return messagebox.showwarning("Aviso", "Selecione um produto.")
        valores = self.tree_produtos.item(sel[0], "values")
        if messagebox.askyesno("Confirmar", f"Deletar '{valores[1]}'?"):
            erro = self.banco_dados.remove_produto(id=int(valores[0]))
            if erro:
                messagebox.showwarning("Aviso", erro)
            else:
                self.carregar_produtos()
                messagebox.showinfo("Sucesso", "Produto deletado!")

    def _show_clientes(self):
        """Tela de cadastro/consulta de clientes."""
        self.clear_main_content()

        page = Frame(self.frame_principal, bg=Color.white.value)
        page.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        self.frame_principal.grid_rowconfigure(1, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)

        Label(page, text="Cadastro de Clientes", font=("Arial", 18, "bold"),
              bg=Color.white.value).grid(row=0, column=0, pady=20)

        # ------------------ Formulário
        form = Frame(page, bg=Color.white.value)
        form.grid(row=1, column=0, sticky="nsew")
        for i in (0, 1):
            form.grid_columnconfigure(i, weight=1)

        self.e_cli_nome  = self._create_label_entry(form, "Nome",     row=0, col=0)
        self.e_cli_tel   = self._create_label_entry(form, "Telefone", row=0, col=1)
        self.e_cli_email = self._create_label_entry(form, "Email",    row=2, col=0)
        self.e_cli_cpf   = self._create_label_entry(form, "CPF",      row=2, col=1)
        self.e_cli_cep   = self._create_label_entry(form, "CEP",      row=4, col=0)

        self._editar_cpf_ref = None  #  guarda CPF original durante edição

        def salvar_cliente():
            nome  = self.e_cli_nome.get().strip()
            tel   = self.e_cli_tel.get().strip()
            email = self.e_cli_email.get().strip()
            cpf   = self.e_cli_cpf.get().strip()
            cep   = self.e_cli_cep.get().strip()

            if not (nome and tel and email and cpf and cep):
                return messagebox.showerror("Erro", "Todos os campos são obrigatórios")

            if self._editar_cpf_ref:
                erro = self.banco_dados.update_usuario(cpf=self._editar_cpf_ref, new_name=nome,
                                                       new_telefone=tel, new_email=email,
                                                       new_cpf=cpf, new_cep=cep)
            else:
                erro = self.banco_dados.add_pessoa(nome, tel, email, cpf, cep)

            if erro:
                messagebox.showerror("Erro", erro)
            else:
                msg = "atualizado" if self._editar_cpf_ref else "adicionado"
                messagebox.showinfo("Sucesso", f"Cliente {msg} com sucesso!")
                self._editar_cpf_ref = None
                self._carregar_clientes()

        Button(form, text="Salvar", bg=Color.light_blue.value, fg="white",
               font=("Arial", 12, "bold"), command=salvar_cliente).grid(row=5, column=1, pady=20)

        # ------------------ Treeview
        tree_frame = Frame(page)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        page.grid_rowconfigure(2, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        cols = ("nome", "telefone", "email", "cpf", "cep")
        self.tree_cli = ttk.Treeview(tree_frame, columns=cols, show="headings")
        for col in cols:
            self.tree_cli.heading(col, text=col.upper())
            self.tree_cli.column(col, width=100, anchor="center")
        self.tree_cli.grid(row=0, column=0, sticky="nsew")

        scroll_cli = Scrollbar(tree_frame, orient="vertical", command=self.tree_cli.yview)
        scroll_cli.grid(row=0, column=1, sticky="ns")
        self.tree_cli.configure(yscrollcommand=scroll_cli.set)

        # ------------------ Botões extra
        def preencher_para_edicao():
            item = self.tree_cli.focus()
            if not item:
                return messagebox.showwarning("Aviso", "Selecione um cliente.")
            valores = self.tree_cli.item(item, "values")
            self._editar_cpf_ref = valores[3]
            self.e_cli_nome.delete(0, END);  self.e_cli_nome.insert(0, valores[0])
            self.e_cli_tel.delete(0, END);   self.e_cli_tel.insert(0, valores[1])
            self.e_cli_email.delete(0, END); self.e_cli_email.insert(0, valores[2])
            self.e_cli_cpf.delete(0, END);   self.e_cli_cpf.insert(0, valores[3])
            self.e_cli_cep.delete(0, END);   self.e_cli_cep.insert(0, valores[4])

        def excluir_cliente():
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
                    self._carregar_clientes()

        b_frame = Frame(page, bg=Color.white.value)
        b_frame.grid(row=3, column=0, pady=10)
        Button(b_frame, text="Editar", bg="#FFA500", fg="white",
               command=preencher_para_edicao).pack(side=LEFT, padx=10)
        Button(b_frame, text="Excluir", bg="#FF4444", fg="white",
               command=excluir_cliente).pack(side=LEFT, padx=10)

        # ------------------ Busca por CPF
        busca_frame = Frame(page, bg=Color.white.value)
        busca_frame.grid(row=4, column=0, pady=10)
        Label(busca_frame, text="CPF:", bg=Color.white.value).pack(side=LEFT)
        busca_entry = Entry(busca_frame)
        busca_entry.pack(side=LEFT, padx=5)

        def buscar_por_cpf():
            cpf = busca_entry.get().strip()
            for cli in self.banco_dados.listar_clientes():
                if cli[3] == cpf:
                    self._editar_cpf_ref = cli[3]
                    self.e_cli_nome.delete(0, END);  self.e_cli_nome.insert(0, cli[0])
                    self.e_cli_tel.delete(0, END);   self.e_cli_tel.insert(0, cli[1])
                    self.e_cli_email.delete(0, END); self.e_cli_email.insert(0, cli[2])
                    self.e_cli_cpf.delete(0, END);   self.e_cli_cpf.insert(0, cli[3])
                    self.e_cli_cep.delete(0, END);   self.e_cli_cep.insert(0, cli[4])
                    return messagebox.showinfo("Sucesso", "Cliente encontrado!")
            messagebox.showinfo("Info", "Cliente não encontrado.")

        def excluir_por_cpf():
            cpf = busca_entry.get().strip()
            if not cpf:
                return messagebox.showwarning("Aviso", "Digite um CPF.")
            if messagebox.askyesno("Confirmar", f"Excluir CPF {cpf}?"):
                erro = self.banco_dados.remove_usuario(cpf)
                if erro:
                    messagebox.showerror("Erro", erro)
                else:
                    messagebox.showinfo("Sucesso", "Cliente excluído!")
                    self._carregar_clientes()

        Button(busca_frame, text="Buscar/Editar", command=buscar_por_cpf,
               bg="#2196F3", fg="white").pack(side=LEFT, padx=5)
        Button(busca_frame, text="Excluir por CPF", command=excluir_por_cpf,
               bg="#D32F2F", fg="white").pack(side=LEFT, padx=5)

        self._carregar_clientes()

    def _carregar_clientes(self):
        self.tree_cli.delete(*self.tree_cli.get_children())
        for cli in self.banco_dados.listar_clientes():
            self.tree_cli.insert("", "end", values=cli)

    # ------------------------------------------------------------------
    #  ★  HELPERS
    # ------------------------------------------------------------------
    def _create_label_entry(self, parent, text, row, col):
        Label(parent, text=text, bg=Color.white.value).grid(row=row, column=col, sticky="w", padx=(0, 5))
        entry = Entry(parent)
        entry.grid(row=row+1, column=col, padx=(0, 5), pady=5, sticky="ew")
        return entry

    def clear_main_content(self):
        """Remove todos os widgets (exceto header) da área de conteúdo."""
        # Mantém o header (row 0); remove a partir do row 1
        for widget in self.frame_principal.winfo_children():
            info = widget.grid_info()
            if info and int(info.get("row", 0)) >= 1:
                widget.destroy()

    def destroy_window(self):
        self.root.destroy()



if __name__ == "__main__":
    root = Tk()
    Application(root)

