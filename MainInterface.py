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

  def layout_sidebar(self):
    self.sidebar = Frame(self.root, width=1000, bg=Color.light_blue.value)
    self.sidebar.pack(side="left", fill="y")

    btn_produtos = self.create_button(self.sidebar, "Produtos", command=None)
    btn_entrada = self.create_button(self.sidebar, "Entradas", command=None)
    btn_saida = self.create_button(self.sidebar, "Saidas", command=None)
    btn_cliente = self.create_button(self.sidebar, "Clientes", command=None)
    
  def create_button(self, frame, text, command):  
    btn = Button(frame, 
                 text=text,
                 command=command, 
                 bg=Color.light_blue.value, 
                 fg=Color.white.value, 
                 borderwidth=0, 
                 highlightthickness= 0, 
                 relief="flat")
    btn.pack(fill="x", pady=5, padx=10)

    return btn
    

  def destroy_window(self):
    root.destroy()        # Destroi a janela do Tkinter

root = Tk()
Application(root)