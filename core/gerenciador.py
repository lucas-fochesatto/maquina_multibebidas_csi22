from core.venda import Venda


class Gerenciador:
    def __init__(self):
        #vamos encapsular tudo aqui, para manter a integridade dos dados
        self.__saldo_total = 0.0
        self.__qtd_vendas = 0
        self.__total_vendido_dosadas = 0.0
        self.__total_vendido_latas = 0.0
        self.__historico_vendas = []
    #getters para acessar os atributos privados
    def get_saldo_total(self) -> float: return self.__saldo_total
    def get_qtd_vendas(self) -> int: return self.__qtd_vendas
    def get_total_vendido_dosadas(self) -> float: return self.__total_vendido_dosadas
    def get_total_vendido_latas(self) -> float: return self.__total_vendido_latas
    def get_historico_vendas(self) -> list: return self.__historico_vendas

    #agora os metodos de acordo com o nosso UMLL
    def registrar_venda(self, venda: Venda):
        #docstring a seguir.
        """Atualiza a contabilidade do sistema após uma venda concluída."""
        if venda.get_status() == "concluida":
            self.__historico_vendas.append(venda)
            self.__qtd_vendas += 1
            #lembrando que para parametros locais nao precisamos usar os getters, mas para acessar os atributos do objeto venda, sim.
            valor_pago = venda.get_pagamento().get_valor()
            self.__saldo_total += valor_pago

            # Lógica para separar os totais por tipo (conforme UML)
            from bebidas.bebida_dosada import BebidaDosada
            if isinstance(venda.get_bebida(), BebidaDosada):
                self.__total_vendido_dosadas += valor_pago
            else:
                self.__total_vendido_latas += valor_pago

    def relatorio(self) -> dict:
        #docstring pra ajudar na visualizacao nos outros files
        """Retorna um dicionário com o resumo financeiro."""
        return {
            "saldo": self.__saldo_total,
            "vendas": self.__qtd_vendas,
            "dosadas": self.__total_vendido_dosadas,
            "latas": self.__total_vendido_latas
        }