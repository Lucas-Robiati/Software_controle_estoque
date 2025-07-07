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
    self.root.title("InerCalc")                                  # Nome do software
    self.root.configure(background= Color.dark_blue.value)       # Background da janela principal
    self.root.geometry("950x520")                                # Geometria da janela 
    self.root.minsize(width=950, height=520)                     # Tamanho minimo da janela 
    self.root.resizable(True,True)                               # Software pode redimensionar 
    self.root.protocol('WM_DELETE_WINDOW', self.destroy_window)

  
  def destroy_window(self):
    root.destroy()        # Destroi a janela do Tkinter

root = Tk()
Application(root)