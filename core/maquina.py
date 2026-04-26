from auth.decorators import auth
from bebidas.bebida import Bebida
from bebidas.bebida_dosada import BebidaDosada
from bebidas.bebida_lata import BebidaLata
from core.estoque import Estoque
from pagamentos.pagamento import Pagamento
from core.venda import Venda
from core.gerenciador import Gerenciador

class MaquinaCafeMB:
  def __init__(self, estoque, gerenciador, dispensadores=None):
    self.__ligada = False
    self.__nivel_limpeza = 100
    self.__estoque : Estoque = estoque
    self.__gerenciador : Gerenciador = gerenciador
    self.__dispensadores = dispensadores if dispensadores is not None else []
    self.__bebidas_disponiveis = []

    self.__admin_login = "admin"
    self.__admin_senha = "ita2026"
  
  def _autenticar(self, login, senha):
    return login == self.__admin_login and senha == self.__admin_senha

  def ligar(self):
    if self.__ligada:
      print("A máquina já está ligada.")
      return
    self.__ligada = True
    print("Maquina ligada.")

  def desligar(self):
    if not self.__ligada:
      print("A máquina já está desligada.")
      return
    self.__ligada = False
    print("Máquina desligada.")

  def consultar_bebidas(self):
    if not self.__ligada:
      print("A máquina está desligada.")
      return
    
    print("\n=== CARDÁPIO ===")
    print("-" * 40)

    dosadas = [b for b in self.__bebidas_disponiveis if isinstance(b, BebidaDosada)]
    latas = [b for b in self.__bebidas_disponiveis if isinstance(b, BebidaLata)]
    
    if dosadas:
      print("Bebidas Dosadas (R$ 10,00):")
      for i, b in enumerate(dosadas, 1):
        print(f"  {i}. {b.get_nome()}")

    if latas:
      print("Bebidas em Lata (R$ 5,00):")
      for i, b in enumerate(latas, 1):
        print(f"  {i}. {b.get_nome()}")

    if not dosadas and not latas:
      print("Nenhuma bebida disponível.")

  def limpar(self):
    if not self.__ligada:
      print("A máquina está desligada.")
      return
    
    self.__nivel_limpeza = 100
    print("Máquina limpa com sucesso. Nível de limpeza: 100%")

  def fazer_bebida(self, bebida: Bebida, doses):
    if not self.__ligada:
      print("A máquina está desligada.")
      return
    
    if self.__nivel_limpeza <= 0:
      print("Máquina precisa de limpeza antes de continuar.")
      return
    
    if isinstance(bebida, BebidaDosada):
      if not self.__estoque.tem_copo():
        print("Sem copos disponíveis.")
        return
      if not self.__estoque.tem_ingredientes(bebida.get_receita(), doses):
        print("Ingredientes insuficientes.")
        return
    
      self.__estoque.consumir_copo()
      bebida.preparar(self.__dispensadores, doses)
      self.__nivel_limpeza -= 10

    elif isinstance(bebida, BebidaLata):
      if not self.__estoque.tem_lata(bebida.get_nome()):
        print(f"Sem estoque de {bebida.get_nome()}.")
        return

      bebida.preparar(self.__dispensadores)

  def venda(self, bebida: Bebida, pagamento: Pagamento, doses):
    if not self.__ligada:
      print("A máquina está desligada.")
      return
    
    if bebida not in self.__bebidas_disponiveis:
      print(f"{bebida.get_nome()} não está disponível no cardápio.")
      return None
    
    print(f"\nTotal: R${bebida.get_preco()}")

    venda_registro = Venda(bebida, pagamento)

    if venda_registro.get_status() != "concluida":
      print("Pagamento não aprovado. Venda cancelada.")
      return None

    self.fazer_bebida(bebida, doses)
    self.__gerenciador.registrar_venda(venda_registro)
    print(f"\nVenda concluída com sucesso!")

    return venda_registro

  @auth
  def adicionar_bebida(self, bebida: Bebida):
    self.__bebidas_disponiveis.append(bebida)
    print(f"Bebida '{bebida.get_nome()}' adicionada ao cardápio.")

  @auth
  def remover_bebida(self, bebida: Bebida):
    self.__bebidas_disponiveis.remove(bebida)
    print(f"Bebida '{bebida.get_nome()}' removida do cardápio.")
  
  @auth
  def ver_estoque_atual(self):
    print(self.__estoque)

  @auth
  def atualizar_estoque_latas(self, tipo, latas):
    self.__estoque.reabastecer_latas(tipo, latas)
  
  @auth
  def atualizar_ingrediente(self, nome, quantidade):
    self.__estoque.reabastecer_ingrediente(nome, quantidade)

  @auth
  def ver_relatorio(self):
    relatorio = self.__gerenciador.relatorio()
    for chave, valor in relatorio.items():
      print(f"  {chave}: {valor}")
    return relatorio