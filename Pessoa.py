
class Pessoa:
  def __init__(self, name:str, telefone:str, cpf:str):
    self._name = name
    self._telefone = telefone
    self._cpf = cpf

  @property
  def name(self):
    return self.__name

  @name.setter
  def name(self, name):
    self.__name = name
    return name

  @property
  def telefone(self):
    return self.__telefone

  @name.setter
  def telefone(self, telefone):
    self.__telefone = telefone
    return telefone

  @property
  def cpf(self):
    return self.__cpf

  @cpf.setter
  def cpf(self, cpf):
    self.__cpf = cpf
    return cpf
