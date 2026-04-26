from core.venda import Venda


class Gerenciador:
    def __init__(self):
        self.saldo_total = 0.0
        self.qtd_vendas = 0
        self.total_vendido_dosadas = 0.0
        self.total_vendido_latas = 0.0
        self.historico_vendas = []
    #agora os metodos de acordo com o nosso UMLL
    def registrar_venda(self, venda: Venda):
        #docstring a seguir.
        """Atualiza a contabilidade do sistema após uma venda concluída."""
        if venda.status == "concluida":
            self.historico_vendas.append(venda)
            self.qtd_vendas += 1
            self.saldo_total += venda.pagamento.valor
            
            # Lógica para separar os totais por tipo (conforme UML)
            from bebidas.bebida import Bebida_dosada 
            if isinstance(venda.bebida, Bebida_dosada):
                self.total_vendido_dosadas += venda.pagamento.valor
            else:
                self.total_vendido_latas += venda.pagamento.valor

    def relatorio(self) -> dict:
        #docstring pra ajudar na visualizacao nos outros files
        """Retorna um dicionário com o resumo financeiro."""
        return {
            "saldo": self.saldo_total,
            "vendas": self.qtd_vendas,
            "dosadas": self.total_vendido_dosadas,
            "latas": self.total_vendido_latas
        }