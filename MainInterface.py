from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from Modules import *
from DataBase import Database_conect

class Application(Validate):
    def __init__(self, root: 'Tk'):
        self.root = root
        self.db = Database_conect()
        self.window()
        root.mainloop()

    def window(self):
        self.root.title("Controle de Estoque")
        self.root.configure(background=Color.white.value)
        self.root.geometry("1000x600")
        self.root.minsize(width=950, height=520)
        self.root.resizable(True, True)
        self.root.protocol('WM_DELETE_WINDOW', self.destroy_window)

        self.layout_sidebar()

        self.main_content = Frame(self.root, bg=Color.white.value)
        self.main_content.pack(side="left", fill="both", expand=True)

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def layout_sidebar(self):
        self.sidebar = Frame(self.root, width=200, bg=Color.light_blue.value)
        self.sidebar.pack(side="left", fill="y")

        btn_produtos = self.create_button(self.sidebar, "Produtos", command=None)
        btn_entrada = self.create_button(self.sidebar, "Entradas", command=None)
        btn_saida = self.create_button(self.sidebar, "Saidas", command=None)
        btn_cliente = self.create_button(self.sidebar, "Clientes", command=self.show_clientes)

    def create_button(self, frame, text, command):
        btn = Button(frame,
                     text=text,
                     command=command,
                     bg=Color.light_blue.value,
                     fg=Color.white.value,
                     borderwidth=0,
                     highlightthickness=0,
                     relief="flat")
        btn.pack(fill="x", pady=5, padx=10)
        return btn

    def show_clientes(self):
        self.clear_main_content()

        canvas = Canvas(self.main_content, bg=Color.white.value)
        scrollbar = Scrollbar(self.main_content, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg=Color.white.value)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        Label(scrollable_frame, text="Cadastro de Clientes", font=("Arial", 18, "bold"),
              bg=Color.white.value, fg="black").pack(pady=20)

        form_frame = Frame(scrollable_frame, bg=Color.white.value)
        form_frame.pack(pady=10)

        def create_labeled_entry(label_text):
            Label(form_frame, text=label_text, font=("Arial", 12), bg=Color.white.value).pack(anchor="w", pady=(10, 2))
            entry = Entry(form_frame, font=("Arial", 12), width=40)
            entry.pack()
            return entry

        nome_entry = create_labeled_entry("Nome")
        telefone_entry = create_labeled_entry("Telefone")
        email_entry = create_labeled_entry("Email")
        cpf_entry = create_labeled_entry("CPF")
        cep_entry = create_labeled_entry("CEP")

        editar_cliente_cpf = [None]

        def adicionar_ou_editar_cliente():
            nome = nome_entry.get()
            telefone = telefone_entry.get()
            email = email_entry.get()
            cpf = cpf_entry.get()
            cep = cep_entry.get()

            if not nome or not telefone or not cpf or not email or not cep:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            if editar_cliente_cpf[0]:
                resultado = self.db.update_usuario(cpf=editar_cliente_cpf[0], new_name=nome, new_telefone=telefone, new_email=email, new_cpf=cpf, new_cep=cep)
                if resultado:
                    messagebox.showerror("Erro", resultado)
                else:
                    messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
                    editar_cliente_cpf[0] = None
                    btn_add_cliente.configure(text="Adicionar Cliente", bg=Color.light_blue.value)
            else:
                resultado = self.db.add_pessoa(nome, telefone, email, cpf, cep)
                if resultado:
                    messagebox.showerror("Erro", resultado)
                else:
                    messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")

            nome_entry.delete(0, END)
            telefone_entry.delete(0, END)
            cpf_entry.delete(0, END)
            email_entry.delete(0, END)
            cep_entry.delete(0, END)
            self.show_clientes()

        btn_add_cliente = Button(form_frame, text="Adicionar Cliente", font=("Arial", 12, "bold"),
                                 bg=Color.light_blue.value, fg="white", padx=10, pady=5,
                                 command=adicionar_ou_editar_cliente)
        btn_add_cliente.pack(pady=20)

        tree_frame = Frame(scrollable_frame)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.tree_clientes = ttk.Treeview(tree_frame,
                                          columns=("nome", "telefone", "email", "cpf", "cep"),
                                          show='headings',
                                          yscrollcommand=tree_scroll.set,
                                          height=6)
        tree_scroll.config(command=self.tree_clientes.yview)

        for col in ("nome", "telefone", "email", "cpf", "cep"):
            self.tree_clientes.heading(col, text=col.capitalize())

        self.tree_clientes.pack(fill="both", expand=True)

        for cliente in self.db.listar_clientes():
            self.tree_clientes.insert('', 'end', values=cliente)

        def preencher_campos_para_editar_valores(valores):
            nome_entry.delete(0, END)
            nome_entry.insert(0, valores[0])
            telefone_entry.delete(0, END)
            telefone_entry.insert(0, valores[1])
            email_entry.delete(0, END)
            email_entry.insert(0, valores[2])
            cpf_entry.delete(0, END)
            cpf_entry.insert(0, valores[3])
            cep_entry.delete(0, END)
            cep_entry.insert(0, valores[4])
            editar_cliente_cpf[0] = valores[3]
            btn_add_cliente.configure(text="Confirmar Edição", bg="#FFA500")

            # Simular seleção na treeview
            for item in self.tree_clientes.get_children():
                item_vals = self.tree_clientes.item(item, 'values')
                if len(item_vals) >= 4 and item_vals[3] == valores[3]:
                    self.tree_clientes.selection_set(item)
                    self.tree_clientes.focus(item)
                    self.tree_clientes.see(item)
                    return True
            return False

        def preencher_campos_para_editar():
            selecionado = self.tree_clientes.focus()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
                return
            valores = self.tree_clientes.item(selecionado, 'values')
            preencher_campos_para_editar_valores(valores)

        def excluir_cliente():
            selecionado = self.tree_clientes.focus()
            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
                return

            valores = self.tree_clientes.item(selecionado, 'values')
            cpf = valores[3]
            confirm = messagebox.askyesno("Confirmação", f"Deseja realmente excluir o cliente com CPF {cpf}?")

            if confirm:
                resultado = self.db.excluir_cliente(cpf)
                if resultado:
                    messagebox.showerror("Erro", resultado)
                else:
                    self.tree_clientes.delete(selecionado)
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")

        botoes_frame = Frame(scrollable_frame, bg=Color.white.value)
        botoes_frame.pack(pady=10)

        Button(botoes_frame, text="Editar Cliente", font=("Arial", 12),
               bg="#4CAF50", fg="white", padx=10, command=preencher_campos_para_editar).pack(side=LEFT, padx=10)

        Button(botoes_frame, text="Excluir Selecionado", font=("Arial", 12),
               bg="#f44336", fg="white", padx=10, command=excluir_cliente).pack(side=LEFT, padx=10)

        buscar_frame = Frame(scrollable_frame, bg=Color.white.value)
        buscar_frame.pack(pady=20)

        Label(buscar_frame, text="CPF:", bg=Color.white.value, font=("Arial", 12)).pack(side=LEFT)
        cpf_busca_entry = Entry(buscar_frame, font=("Arial", 12), width=20)
        cpf_busca_entry.pack(side=LEFT, padx=5)

        def buscar_por_cpf():
            cpf = cpf_busca_entry.get()
            if not cpf:
                messagebox.showwarning("Aviso", "Digite um CPF para buscar.")
                return
            clientes = self.db.listar_clientes()
            for cliente in clientes:
                if cliente[3] == cpf:
                    valores = (cliente[0], cliente[1], cliente[2], cliente[3], cliente[4])
                    if preencher_campos_para_editar_valores(valores):
                        messagebox.showinfo("Info", f"Cliente encontrado com CPF {cpf}.")
                    else:
                        messagebox.showinfo("Info", f"Cliente encontrado no banco, mas não foi possível localizar na lista.")
                    return
            messagebox.showinfo("Info", f"Cliente com CPF {cpf} não encontrado no banco de dados.")

        def excluir_por_cpf():
            cpf = cpf_busca_entry.get()
            if not cpf:
                messagebox.showwarning("Aviso", "Digite um CPF para excluir.")
                return
            confirm = messagebox.askyesno("Confirmação", f"Deseja realmente excluir o cliente com CPF {cpf}?")
            if confirm:
                resultado = self.db.excluir_cliente(cpf)
                if resultado:
                    messagebox.showerror("Erro", resultado)
                else:
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
                    self.show_clientes()

        Button(buscar_frame, text="Buscar/Editar", bg="#2196F3", fg="white",
               font=("Arial", 12), command=buscar_por_cpf).pack(side=LEFT, padx=5)
        Button(buscar_frame, text="Excluir por CPF", bg="#FF0000", fg="white",
               font=("Arial", 12), command=excluir_por_cpf).pack(side=LEFT, padx=5)

    def destroy_window(self):
        self.root.destroy()

root = Tk()
Application(root)

