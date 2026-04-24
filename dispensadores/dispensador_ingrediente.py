from .dispensador import Dispensador

class DispensadorIngrediente(Dispensador):
  def __init__(self, ingrediente):
    super().__init__()
    self.__ingrediente = ingrediente

  def acionar(self, percentual):
    self.ativar()
    print(f"  Preparando {self.__ingrediente.get_nome()} a {percentual}%...")

    quantidade_liberada = self.__ingrediente.dispensar(percentual)

    print(f"  {quantidade_liberada}g de {self.__ingrediente.get_nome()} liberados.")
    self.desativar()

    return quantidade_liberada
