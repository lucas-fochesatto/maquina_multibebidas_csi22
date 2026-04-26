from datetime import datetime
from pagamentos.pagamento import Pagamento

class Venda:
    def __init__(self, bebida, pagamento: Pagamento):
        # Agregação: A venda armazena os objetos passados a ela
        self.bebida = bebida
        self.pagamento = pagamento
        
        # Automaticamente define a data da venda
        self.data = datetime.now()
        
        # Executa o pagamento e define o status
        if self.pagamento.processar():
            self.status = "concluida"
        else:
            self.status = "falha_pagamento"

    def comprovante(self) -> str:
        """Gera a string formatada do recibo da transação."""
        linhas = [
            "--- COMPROVANTE ---",
            f"Data: {self.data.strftime('%d/%m/%Y %H:%M:%S')}",
            f"Bebida: {self.bebida.get_nome}",
            f"Total Pago: R$ {self.pagamento.valor:.2f}",
            f"Status: {self.status}",
            "-------------------"
        ]
        return "\n".join(linhas)