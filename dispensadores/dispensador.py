from abc import ABC, abstractmethod

class Dispensador(ABC):
  def __init__(self):
    self.__ativo = False
  
  def ativar(self):
    self.__ativo = True
    print(f"[{self.__class__.__name__}] Ativado.")

  def desativar(self):
    self.__ativo = False
    print(f"[{self.__class__.__name__}] Desativado.")

  @abstractmethod
  def acionar(self, *args, **kwargs):
    pass