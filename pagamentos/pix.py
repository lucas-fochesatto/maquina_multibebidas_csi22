from pagamento import Pagamento

class Pix(Pagamento):
    def  __init__(self, valor: float, chave_destino: str):
        #chama o construtor da classe base Pagamento para inicializar o valor.
        super().__init__(valor)
        #a chave_destino é um atributo específico para o Pix, que representa a chave Pix do destinatário do pagamento
        self.__chave_destino = chave_destino
    
    def get_chave_destino(self) -> str:
        return self.__chave_destino
        
    def processar(self) -> bool:
        #aqui implementamos a lógica de processamento do pagamento via Pix
        print(f"Iniciando transação Pix...")
        print(f"Transferindo R$ {self.get_valor():.2f} para a chave: {self.__chave_destino}")
        #para simplificar, vamos assumir que o pagamento é sempre aprovado :)
        #agora usamos set_aprovado ao inves de acessar diretamente o atributo, para manter o encapsulamento e a consistencia com as outras classes de pagamento
        self.set_aprovado(True)
        print("Pagamento via Pix aprovado!\n")
        
        return self.get_aprovado()