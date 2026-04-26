from abc import ABC, abstractmethod

class Bebida(ABC):
  def __init__(self, nome, preco):
    self.__nome = nome
    self.__preco = preco

  @abstractmethod
  def preparar(self, *args, **kwargs):
    pass

  def get_nome(self):
    return self.__nome

  def get_preco(self):
    return self.__preco