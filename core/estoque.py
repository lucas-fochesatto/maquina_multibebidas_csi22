class Estoque:
  def __init__(self):
    self.__latas = {}
    self.__ingredientes = {}
    self.__copos = 0
  
  def tem_lata(self, tipo):
    return len(self.__latas.get(tipo, [])) > 0
  
  def tem_ingredientes(self, receita, doses):
    gramas_necessarias = receita.custo_em_gramas(doses)
    for ingrediente, gramas in gramas_necessarias.items():
      if ingrediente.get_quantidade() < gramas:
        return False
    return True
  
  def tem_copo(self):
    return self.__copos > 0
  
  def retirar_lata(self, tipo):
    if not self.tem_lata(tipo):
      print(f"Sem estoque de {tipo}")
      return
    lata = self.__latas[tipo].pop()
    print(f"  [Estoque] Lata de {tipo} retirada. Restam: {len(self.__latas[tipo])}")
    return lata
  
  def consumir_ingredientes(self, receita, doses):
    if not self.tem_ingredientes(receita, doses):
      print("Ingredientes insuficientes.")
      return
    gramas = receita.custo_em_gramas(doses)
    for ingrediente, qtd in gramas.items():
      ingrediente.dispensar(round((qtd / ingrediente.get_porcao_padrao()) * 100))
    
  def consumir_copo(self):
    if not self.tem_copo():
      print("Sem copos disponíveis")
      return
    self.__copos -= 1
    print(f"  [Estoque] Copo retirado. Restam: {self.__copos}")
  
  def reabastecer_latas(self, tipo, latas):
    if tipo not in self.__latas:
      self.__latas[tipo] = []
    self.__latas[tipo].extend(latas)
    print(f"  [Estoque] {len(latas)} latas de {tipo} adicionadas. Total: {len(self.__latas[tipo])}")

  def reabastecer_ingrediente(self, nome, quantidade):
    if nome not in self.__ingredientes:
      print(f"Ingrediente {nome} não cadastrado.")
      return
    self.__ingredientes[nome].reabastecer(quantidade)
    print(f"  [Estoque] {nome} reabastecido com {quantidade}g. Nível: {self.__ingredientes[nome].nivel():.0f}%")
  
  def reabastecer_copos(self, quantidade):
    self.__copos += quantidade
    print(f"  [Estoque] {quantidade} copos adicionados. Total: {self.__copos}")

  def cadastrar_ingrediente(self, ingrediente):
    self.__ingredientes[ingrediente.get_nome()] = ingrediente
    print(f"  [Estoque] Ingrediente '{ingrediente.get_nome()}' cadastrado.")

  def get_ingredientes(self):
    return self.__ingredientes

  def __str__(self):
    linhas = ["=== ESTOQUE ==="]
    linhas.append(f"Copos: {self.__copos}")
    linhas.append("Latas:")
    for tipo, lista in self.__latas.items():
      linhas.append(f"  {tipo}: {len(lista)} unidades")
    linhas.append("Ingredientes:")
    for nome, ing in self.__ingredientes.items():
      linhas.append(f"  {nome}: {ing.get_quantidade()}g / {ing.get_capacidade_maxima()}g ({ing.nivel():.0f}%)")
    return "\n".join(linhas)