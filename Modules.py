import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
from dotenv import load_dotenv
import numpy as np
from enum import Enum
import os

from Pessoa import Pessoa

load_dotenv()

class Color(Enum):
  gray = "#5e5c64"          # Cor Cinza
  light_gray = "#868687"    # Cor Cinza Claro
  dark_blue = "#18304a"     # Cor Azul Escuro
  light_blue = "#0251a1"    # Cor Azul Claro
  aqua_blue = "#033f70"     # Cor Verde Agua
  white = "#e8e8ed"         # Cor White
  black = "#000000"         # Cor Preto

class Validate:
  def validate_cpf(self, text):
    value = 0

    if ((text == "CPF")): return True 

    if ((len(text) == 10) and (text == "-")): return True # Passou na validação
    
    if(len(text) < 10):
      try:
        value == int(text)
      except ValueError:
        return False    
    if( 10 < len(text) <= 12): return True                              # Não passou na validação
    
    return (value)             # Retorna o valor valido