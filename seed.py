from bebidas.bebida_dosada import BebidaDosada
from bebidas.bebida_lata import BebidaLata
from bebidas.ingrediente import Ingrediente
from bebidas.receita import Receita
from core.estoque import Estoque
from core.gerenciador import Gerenciador
from core.maquina import MaquinaCafeMB
from dispensadores.dispensador_ingrediente import DispensadorIngrediente
from dispensadores.dispensador_lata import DispensadorLata


def criar_maquina_populada():
    estoque = Estoque()
    gerenciador = Gerenciador()

    cafe = Ingrediente("Café", quantidade=400, capacidade_maxima=500, porcao_padrao=10.0)
    leite = Ingrediente("Leite", quantidade=400, capacidade_maxima=500, porcao_padrao=20.0)
    acucar = Ingrediente("Açúcar", quantidade=200, capacidade_maxima=300, porcao_padrao=5.0)
    chocolate = Ingrediente("Chocolate", quantidade=300, capacidade_maxima=400, porcao_padrao=15.0)
    canela = Ingrediente("Canela", quantidade=80, capacidade_maxima=100, porcao_padrao=2.0)

    estoque.cadastrar_ingrediente(cafe)
    estoque.cadastrar_ingrediente(leite)
    estoque.cadastrar_ingrediente(acucar)
    estoque.cadastrar_ingrediente(chocolate)
    estoque.cadastrar_ingrediente(canela)

    estoque.reabastecer_copos(15)

    cappuccino = BebidaDosada(
        "Cappuccino",
        preco=8.0,
        receita=Receita({cafe: 100, leite: 70, acucar: 30}),
    )
    cafe_com_leite = BebidaDosada(
        "Café com Leite",
        preco=6.0,
        receita=Receita({cafe: 70, leite: 100}),
    )
    mocha = BebidaDosada(
        "Mocha",
        preco=9.0,
        receita=Receita({cafe: 70, leite: 70, chocolate: 100}),
    )
    chocolate_quente = BebidaDosada(
        "Chocolate Quente",
        preco=7.0,
        receita=Receita({leite: 100, chocolate: 100, canela: 50}),
    )

    coca = BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350)
    guarana = BebidaLata("Guaraná", preco=5.5, marca="Antarctica", volume_ml=350)
    pepsi = BebidaLata("Pepsi", preco=5.5, marca="Pepsi", volume_ml=350)

    estoque.reabastecer_latas("Coca-Cola", [
        BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350) for _ in range(5)
    ])
    estoque.reabastecer_latas("Guaraná", [
        BebidaLata("Guaraná", preco=5.5, marca="Antarctica", volume_ml=350) for _ in range(4)
    ])
    estoque.reabastecer_latas("Pepsi", [
        BebidaLata("Pepsi", preco=5.5, marca="Pepsi", volume_ml=350) for _ in range(3)
    ])

    dispensadores = [
        DispensadorIngrediente(cafe),
        DispensadorIngrediente(leite),
        DispensadorIngrediente(acucar),
        DispensadorIngrediente(chocolate),
        DispensadorIngrediente(canela),
        DispensadorLata("Coca-Cola", estoque),
        DispensadorLata("Guaraná", estoque),
        DispensadorLata("Pepsi", estoque),
    ]

    cardapio_inicial = [cappuccino, cafe_com_leite, mocha, chocolate_quente, coca, guarana, pepsi]

    maquina = MaquinaCafeMB(estoque, gerenciador, dispensadores, bebidas_iniciais=cardapio_inicial)
    maquina.ligar()

    return maquina
