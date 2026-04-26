from pagamento import Pagamento
#importamos da classe abstrata.
class CartaoDebito(Pagamento):
    #iniciamos o construtor com seus argumentos especificos
    def __init__(self,valor: float, numero: str, titular: str, validade: str, cvv: str):
        super().__init__(valor)
        self.numero = numero
        self.titular = titular
        self.validade = validade
        self.cvv = cvv
    #aqui implementamos o metodo processar, que era abstrato na classe Pagamento, e agora tem uma implementacao concreta para o CartaoDebito
    def processar(self) -> bool:
        print("Processando pagamento com cartão de débito...")
        print(f"verificando saldo para {self.titular} || Valor: R$ {self.valor:.2f}")
        #simulamos uma conexao a conta de banco, mas aqui sempre aprovamos o pagamento, para fins didaticos
        self.aprovado = True
        print("Transação de debito aprovada!\n")
        return self.aprovado