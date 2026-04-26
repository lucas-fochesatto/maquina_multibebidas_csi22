from pagamento import Pagamento

class CartaoCredito(Pagamento):
    def __init__(self, valor: float, numero: str, titular: str, validade: str, cvv: str ):
        #mesmo procedimento das demais classes:
        super().__init__(valor)
        #agora os especificos do cartao de credito:
        self.__numero = numero
        self.__titular = titular
        self.__validade = validade
        self.__cvv = cvv
        #getters:
        def get_numero(self) -> str:
            return self.__numero
        def get_titular(self) -> str:
            return self.__titular
        def get_validade(self) -> str:
            return self.__validade
        def get_cvv(self) -> str:
            return self.__cvv
    #implementacao do metodo processar, que simula a verificacao do pagamento:
    def processar(self) -> bool:
        print("Processando pagamento com cartão de crédito...")
        print(f"Verificando limite para {self.get_titular()} || Valor: R$ {self.get_valor():.2f}")
        #simulamos uma conexao API para a operadora de cartao, mas aqui sempre aprovamos o pagamento :)
        self.set_aprovado(True)
        print("Transação de crédito aprovada!\n")
        
        return self.get_aprovado()
