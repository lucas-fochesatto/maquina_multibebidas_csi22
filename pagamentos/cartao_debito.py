from pagamentos.pagamento import Pagamento
#importamos da classe abstrata.
class CartaoDebito(Pagamento):
    #iniciamos o construtor com seus argumentos especificos
    def __init__(self,valor: float, numero: str, titular: str, validade: str, cvv: str):
        super().__init__(valor)
        #vamos usar __ para deixar os atributos privados, seguindo o mesmo padrao das outras classes, para manter a consistencia e o encapsulamento
        self.__numero = numero
        self.__titular = titular
        self.__validade = validade
        self.__cvv = cvv

    #agora precisamos criar os getters para acessar esses atributos privados, caso seja necessario em algum momento do processamento do pagamento
    def get_numero(self) -> str:
        return self.__numero

    def get_titular(self) -> str:
        return self.__titular

    def get_validade(self) -> str:
        return self.__validade

    def get_cvv(self) -> str:
        return self.__cvv

    #o metodo processar aqui tem uma implementacao concreta, que simula a verificacao.
    #aqui implementamos o metodo processar, que era abstrato na classe Pagamento, e agora tem uma implementacao concreta para o CartaoDebito
    def processar(self) -> bool:
        print("Processando pagamento com cartão de débito...")
        #agora usamos os getters para acessar os atributos privados e simular a verificacao do saldo:
        print(f"verificando saldo para {self.get_titular()} || Valor: R$ {self.get_valor():.2f}")
        #simulamos uma conexao a conta de banco, mas aqui sempre aprovamos o pagamento, para fins didaticos
        self.set_aprovado(True)
        print("Transação de debito aprovada!\n")
        return self.get_aprovado()