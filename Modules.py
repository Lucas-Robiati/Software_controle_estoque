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
    if text == "":
        return True
    try:
        float(text)
        return True
    except ValueError:
        return False
 
  def validate_int(self, text):
    if text == "":
        return True
    try:
        int(text)
        return True
    except ValueError:
        return False

  def validate_cpf_entry(self, inserted_char, index, full_text):
    try:
        index = int(index)
    except ValueError:
        return False

    # Restringe o tamanho máximo a 14 caracteres
    if len(full_text) > 14:
        return False

    # Permite texto vazio para edição parcial
    if inserted_char == "":
        return True

    # Se índice 3 ou 7, só permite ponto
    if index in [3, 7]:
        return inserted_char == "."

    # Se índice 11, só permite hífen
    if index == 11:
        return inserted_char == "-"

    # Em outras posições, só números
    if index not in [3, 7, 11]:
        return inserted_char.isdigit()

    # Qualquer outra condição inválida
    return False





  def validate_cpf_entr(self, text):
    # Permite string vazia ou caracteres únicos especiais durante edição
    if text in ["", ".", "-"]:
        return True
        
    # Verifica se todos os caracteres são permitidos
    for char in text:
        if not (char.isdigit() or char in ['.', '-']):
            return False
            
    # Verifica posicionamento correto dos caracteres especiais
    for i, char in enumerate(text):
        if char in ['.', '-']:
            if i not in [3, 7, 11]:  # Posições válidas para '.' e '-'
                return False
                
    # Verifica quantidade máxima de caracteres
    if len(text) > 14:
        return False
        
    # Verifica formatação parcial
    parts = text.replace('-', '.').split('.')
    for i, part in enumerate(parts[:-1]):
        if part != '' and len(part) > 3:
            return False
            
    return True

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