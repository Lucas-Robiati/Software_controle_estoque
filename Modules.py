import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT 
from dotenv import load_dotenv
import numpy as np
from enum import Enum
import os
import re

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
    # melhor usar em tudo, vou fazer um validador de inteiro e float pra alguns campos tenho pronto kkkkkkk
  def format_str(text:str) -> str:
    formatted_text = " ".join(text.split())
    return formatted_text

  def validate_float(self, text):
    value = 0

    if ((text == "") or (text == "-")): return True # Passou na validação
    try:
      value == float(text)
    except ValueError:
      return False                                  # Não passou na validação
    return (0 <= value) or (0 >= value) 

  def validate_cpf_entry(text):
    value = 0

    if ((text == "CPF")): return True 

    if ((len(text) == 10) and (text == "-")): return True # Passou na validação
    
    if (text == "." or text == ""): return True
    
    if(len(text) < 10):
      try:
        value == int(text)
      except ValueError:
        return False      
    return (value)

  def validate_cpf(cpf: str) -> bool:
    # Expressão regular para formato exato 000.000.000-00
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
        return False

    numeros = [int(char) for char in cpf if char.isdigit()]
    
    if all(x == numeros[0] for x in numeros):
        return False

    soma = sum(numeros[i] * (10 - i) for i in range(9))
    digito1 = (soma * 10 % 11) % 10
    
    soma = sum(numeros[i] * (11 - i) for i in range(10))
    digito2 = (soma * 10 % 11) % 10

    return numeros[9] == digito1 and numeros[10] == digito2