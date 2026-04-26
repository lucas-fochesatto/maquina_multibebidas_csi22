from abc import ABC, abstractmethod
#a linha acima importa a classe ABC (Abstract Base Class) usada para criar classes abstratas.
#A classe Pagamento é definida como uma classe abstrata, o que significa que ela não pode ser instanciada diretamente
# afinal ninguem paga na vida real com o mero conceito de pagamento, mas sim com cartao pix etc
class Pagamento(ABC):
    def __init__(self, valor: float):
        self.__valor = valor
        #vamos comecar com aprovado como falso, e so depois de processar o pagamento que ele pode ser aprovado ou nao
        self.__aprovado = False

    #vamos precisar usar getters agora, porque a equipe escolheu tratar os atributos como privados (com __) para garantir o encapsulamento
    #seguindo um excelente padrao de boas praticas:
    def get_valor(self) -> float:
        return self.__valor

    def get_aprovado(self) -> bool:
        return self.__aprovado

    #definiremos tambem um setter para o atributo aprovado, para que as subclasses possam atualizar esse status depois de processar o pagamento
    def set_aprovado(self, status: bool):
        self.__aprovado = status

    #o decorator @abstractmethod indica que o metodo processar deve ser implementado por qualquer classe que herde de Pagamento
    @abstractmethod
    def processar(self) -> bool:
        """Processa o pagamento, mas so eh implementado pelas subclasses"""
        pass