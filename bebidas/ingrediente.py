class Ingrediente():
  def __init__(self, nome, quantidade, capacidade_maxima, porcao_padrao=10.0):
    self.__nome = nome
    self.__quantidade = quantidade
    self.__capacidade_maxima = capacidade_maxima
    self.__porcao_padrao = porcao_padrao

  def dispensar(self, percentual):
    quantidade_liberar = self.__porcao_padrao * (percentual / 100)

    if self.__quantidade < quantidade_liberar:
      print(f"Estoque insuficiente de {self.__nome}")
      return 0

    self.__quantidade -= quantidade_liberar
    return quantidade_liberar

  def reabastecer(self, quantidade):
    quantidade_final = self.__quantidade + quantidade

    if quantidade_final > self.__capacidade_maxima:
      print(f"Quantidade excede a capacidade máxima para {self.__nome}")
      return
    
    self.__quantidade = quantidade_final
    print(f"Estoque reabastecido para {self.__nome}. Estoque final: {self.__quantidade}")

  def nivel(self):
    nivel_preenchimento = self.__quantidade / self.__capacidade_maxima * 100

    return nivel_preenchimento
  
  def get_nome(self):
    return self.__nome
  
  def get_quantidade(self):
    return self.__quantidade
  
  def get_capacidade_maxima(self):
    return self.__capacidade_maxima
  
  def get_porcao_padrao(self):
    return self.__porcao_padrao