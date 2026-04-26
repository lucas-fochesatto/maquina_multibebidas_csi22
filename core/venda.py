from datetime import datetime
from pagamentos.pagamento import Pagamento

class Venda:
    def __init__(self, bebida, pagamento: Pagamento):
        # Agregação: A venda armazena os objetos passados a ela
        self.__bebida = bebida
        self.__pagamento = pagamento

        # Automaticamente define a data da venda
        self.__data = datetime.now()
        
        # Executa o pagamento e define o status
        if self.__pagamento.processar():
            self.__status = "concluida"
        else:
            self.__status = "falha_pagamento"
    # getters:
    def get_bebida(self):        return self.__bebida
    def get_pagamento(self):      return self.__pagamento
    def get_data(self):           return self.__data
    def get_status(self):         return self.__status

    def comprovante(self) -> str:
        """Gera a string formatada do recibo da transação."""
        linhas = [
            "--- COMPROVANTE ---",
            f"Data: {self.__data.strftime('%d/%m/%Y %H:%M:%S')}",
            f"Bebida: {self.__bebida.get_nome()}",
            f"Total Pago: R$ {self.__pagamento.get_valor():.2f}",
            f"Status: {self.__status}",
            "-------------------"
        ]
        return "\n".join(linhas)