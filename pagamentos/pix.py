from pagamento import Pagamento

class Pix(Pagamento):
    def  __init__(self, valor: float, chave_destino: str):
        #chama o construtor da classe base Pagamento para inicializar o valor.
        super().__init__(valor)
        #a chave_destino é um atributo específico para o Pix, que representa a chave Pix do destinatário do pagamento
        self.chave_destino = chave_destino
    def processar(self) -> bool:
        #aqui implementamos a lógica de processamento do pagamento via Pix
        print(f"Iniciando transação Pix...")
        print(f"Transferindo R$ {self.valor:.2f} para a chave: {self.chave_destino}")
        #para simplificar, vamos assumir que o pagamento é sempre aprovado :)
        self.aprovado = True
        print("Pagamento via Pix aprovado!\n")
        return self.aprovado
