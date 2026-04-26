from dispensadores.dispensador_ingrediente import DispensadorIngrediente

from .bebida import Bebida

class BebidaDosada(Bebida):
  def __init__(self, nome, preco, receita):
    super().__init__(nome, preco)
    self.__receita = receita

  def get_receita(self):
    return self.__receita

  def preparar(self, dispensadores, doses = None):
    # doses: {ingrediente: percentual}
    # ex: {cafe: 100, leite: 70, acucar: 30}
    # Se None, usa os percentuais padrão da receita
    for ingrediente, percentual_padrao in self.__receita.get_ingredientes().items():
      # Se o usuário personalizou, usa o dele; senão, usa o padrão
      percentual = doses.get(ingrediente, percentual_padrao) if doses else percentual_padrao

      # Encontra o dispensador certo pra esse ingrediente
      dispensador = None
      for d in dispensadores:
        if isinstance(d, DispensadorIngrediente) and d.get_ingrediente() == ingrediente:
          dispensador = d
          break

      if dispensador is None:
        print(f"  Sem dispensador para {ingrediente.get_nome()}, pulando.")
        continue

      dispensador.acionar(percentual)