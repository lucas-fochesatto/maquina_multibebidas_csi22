from .bebida import Bebida
from dispensadores.dispensador_lata import DispensadorLata

class BebidaLata(Bebida):
  def __init__(self, nome, preco, marca, volume_ml):
    super().__init__(nome, preco)
    self.__marca = marca
    self.__volume_ml = volume_ml

  def preparar(self, dispensadores):
    print(f"\nLiberando {self.get_nome()} ({self.__marca}, {self.__volume_ml}ml)...")

    dispensador = None
    for d in dispensadores:
      if isinstance(d, DispensadorLata) and d.get_tipo_lata() == self.get_nome():
        dispensador = d
        break
    if dispensador is None:
      print(f"  Sem dispensador para {self.get_nome()}, pulando.")
      return None

    return dispensador.acionar()
