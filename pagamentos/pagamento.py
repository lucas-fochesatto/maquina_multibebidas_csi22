from abc import ABC, abstractmethod
#a linha acima importa a classe ABC (Abstract Base Class) usada para criar classes abstratas.
#A classe Pagamento é definida como uma classe abstrata, o que significa que ela não pode ser instanciada diretamente
# afinal ninguem paga na vida real com o mero conceito de pagamento, mas sim com cartao pix etc
class Pagamento(ABC):
    def __init__(self, valor: float):
        self.valor = valor
        self.aprovado = False
        #vamos comecar com aprovado como falso, e so depois de processar o pagamento que ele pode ser aprovado ou nao
        #o decorator @abstractmethod indica que o metodo processar deve ser implementado por qualquer classe que herde de Pagamento
    @abstractmethod
    def processar(self) -> bool:
        """Processa o pagamento, mas so eh implementado pelas subclasses"""
        pass