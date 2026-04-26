from .dispensador import Dispensador

class DispensadorLata(Dispensador):
  def __init__(self, tipo_lata, estoque):
    super().__init__()
    self.__tipo_lata = tipo_lata
    self.__estoque = estoque

  def acionar(self):
    self.ativar()
    print(f"  Liberando lata de {self.__tipo_lata}...")

    if not self.__estoque.tem_lata(self.__tipo_lata):
      self.desativar()
      print(f"Sem estoque de {self.__tipo_lata}")
      return
    
    lata = self.__estoque.retirar_lata(self.__tipo_lata)

    print(f"  Lata de {lata.get_nome()} dispensada.")
    self.desativar()
    return lata

  def get_tipo_lata(self):
    return self.__tipo_lata