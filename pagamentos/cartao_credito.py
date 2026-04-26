from pagamento import Pagamento

class CartaoCredito(Pagamento):
    def __init__(self, valor: float, numero: str, titular: str, validade: str, cvv: str ):
        #mesmo procedimento das demais classes:
        super().__init__(valor)
        #agora os especificos do cartao de credito:
        self.numero = numero
        self.titular = titular
        self.validade = validade
        self.cvv = cvv
    def processar(self) -> bool:
        print("Processando pagamento com cartão de crédito...")
        print(f"Verificando limite para {self.titular} || Valor: R$ {self.valor:.2f}")
        #simulamos uma conexao API para a operadora de cartao, mas aqui sempre aprovamos o pagamento :)
        self.aprovado = True
        print("Transação de crédito aprovada!\n")
        
        return self.aprovado
