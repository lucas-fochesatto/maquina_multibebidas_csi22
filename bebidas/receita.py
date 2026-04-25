class Receita():
  def __init__(self, ingredientes):
    # ingredientes: {ingrediente1: percentual_padrao1, ingrediente2: perentual_padrao2}
    self.__ingredientes = ingredientes
  
  def custo_em_gramas(self, doses):
    resultado = {}

    for ingrediente, percentual_padrao in self.__ingredientes.items():
      percentual = doses.get(ingrediente, percentual_padrao) if doses else percentual_padrao
      resultado[ingrediente] = ingrediente.get_porcao_padrao() * percentual / 100
    return resultado
  
  def ajustar_dose(self, ingrediente, percentual):
    if ingrediente not in self.__ingredientes:
      print(f"{ingrediente.get_nome()} não faz parte desta receita.")
      return
    if percentual not in [30, 50, 70, 100]:
      print("Percentual deve ser 30, 50, 70 ou 100.")
      return
    self.__ingredientes[ingrediente] = percentual

  def get_ingredientes(self):
    return self.__ingredientes

  def __str__(self):
    linhas = []
    for ingrediente, percentual in self.__ingredientes.items():
      gramas = ingrediente.get_porcao_padrao() * (percentual / 100)
      linhas.append(f"  {ingrediente.get_nome()}: {percentual}% ({gramas}g)")
    return "\n".join(linhas)