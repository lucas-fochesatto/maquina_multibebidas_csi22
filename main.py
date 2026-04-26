from bebidas.bebida_dosada import BebidaDosada
from bebidas.bebida_lata import BebidaLata
from bebidas.ingrediente import Ingrediente
from bebidas.receita import Receita
from core.estoque import Estoque
from dispensadores.dispensador_ingrediente import DispensadorIngrediente
from dispensadores.dispensador_lata import DispensadorLata

print("1. Criando ingredientes")
cafe = Ingrediente("Café", quantidade=200, capacidade_maxima=500, porcao_padrao=10.0)
leite = Ingrediente("Leite", quantidade=300, capacidade_maxima=500, porcao_padrao=20.0)
print(f"Nível café:  {cafe.nivel():.1f}%")
print(f"Nível leite: {leite.nivel():.1f}%")

print("\n\n2. Dispensar direto pelo Ingrediente")
liberado = cafe.dispensar(50)
print(f"Liberado: {liberado}g | Nível café: {cafe.nivel():.1f}%")

print("\n\n3. Reabastecer (caso válido + caso excedendo capacidade)")
cafe.reabastecer(50)
cafe.reabastecer(10000)

print("\n\n4. Dispensar com estoque insuficiente")
quase_vazio = Ingrediente("Açúcar", quantidade=1, capacidade_maxima=100, porcao_padrao=10.0)
quase_vazio.dispensar(100)

print("\n\n5. Receita: custo em gramas (dose padrão e dose customizada)")
receita = Receita({cafe: 100, leite: 50})
print("Receita:")
print(receita)

print("\nCusto com doses padrão:")
for ing, gramas in receita.custo_em_gramas(None).items():
    print(f"  {ing.get_nome()}: {gramas}g")

print("\nCusto com leite a 100% (override):")
for ing, gramas in receita.custo_em_gramas({leite: 100}).items():
    print(f"  {ing.get_nome()}: {gramas}g")

print("\n\n6. Ajustar dose (válido, percentual inválido, ingrediente fora)")
receita.ajustar_dose(cafe, 70)
print("Após ajustar café para 70%:")
print(receita)

receita.ajustar_dose(cafe, 42)
fora = Ingrediente("Chocolate", quantidade=100, capacidade_maxima=200, porcao_padrao=15.0)
receita.ajustar_dose(fora, 50)

print("\n\n7. DispensadorIngrediente.acionar()")
dispensador_cafe = DispensadorIngrediente(cafe)
dispensador_cafe.acionar(70)
print(f"Nível café após acionar: {cafe.nivel():.1f}%")

print("\n\n8. BebidaDosada.preparar() — 3 cenários do doses.get()")
dispensador_leite = DispensadorIngrediente(leite)
cappuccino = BebidaDosada("Cappuccino", preco=8.0, receita=Receita({cafe: 100, leite: 70}))
dispensadores = [dispensador_cafe, dispensador_leite]

print("\n8.1 Sem doses (None) — usa padrão da receita (café 100%, leite 70%)")
cappuccino.preparar(dispensadores)

print("\n8.2 Override só do café — leite cai no padrão da receita")
cappuccino.preparar(dispensadores, doses={cafe: 30})

print("\n8.3 Override de todos os ingredientes")
cappuccino.preparar(dispensadores, doses={cafe: 100, leite: 100})

print("\n8.4 Estoque insuficiente — fluxo continua sem quebrar")
doce = BebidaDosada("Doce", preco=5.0, receita=Receita({quase_vazio: 100, cafe: 50}))
dispensador_acucar = DispensadorIngrediente(quase_vazio)
doce.preparar([dispensador_acucar, dispensador_cafe])

print("\n8.5 Receita com ingrediente sem dispensador correspondente")
exotico = Ingrediente("Canela", quantidade=50, capacidade_maxima=100, porcao_padrao=5.0)
mocha = BebidaDosada("Mocha", preco=9.0, receita=Receita({cafe: 70, exotico: 50}))
mocha.preparar(dispensadores)  # falta dispensador de canela: deve pular sem quebrar

print("\n\n9. Estoque — cadastrar e reabastecer ingrediente")
estoque = Estoque()
estoque.cadastrar_ingrediente(cafe)
estoque.cadastrar_ingrediente(leite)

print("\n9.1 Reabastecer ingrediente cadastrado")
estoque.reabastecer_ingrediente("Café", 50)

print("\n9.2 Reabastecer ingrediente não cadastrado")
estoque.reabastecer_ingrediente("Inexistente", 100)

print("\n\n10. Estoque — copos")
estoque.reabastecer_copos(3)
print(f"Tem copo? {estoque.tem_copo()}")
estoque.consumir_copo()
estoque.consumir_copo()
estoque.consumir_copo()
print(f"Tem copo? {estoque.tem_copo()}")

print("\n10.1 Consumir copo sem estoque")
estoque.consumir_copo()

print("\n\n11. Estoque — tem_ingredientes / consumir_ingredientes")
receita_estoque = Receita({cafe: 70, leite: 50})

print("\n11.1 Caso OK")
print(f"Tem ingredientes? {estoque.tem_ingredientes(receita_estoque, None)}")
print(f"Antes — Café: {cafe.get_quantidade()}g | Leite: {leite.get_quantidade()}g")
estoque.consumir_ingredientes(receita_estoque, None)
print(f"Depois — Café: {cafe.get_quantidade()}g | Leite: {leite.get_quantidade()}g")

print("\n11.2 Caso insuficiente (quase_vazio com 1g, receita pede 10g)")
receita_excessiva = Receita({quase_vazio: 100})
print(f"Tem ingredientes? {estoque.tem_ingredientes(receita_excessiva, None)}")
estoque.consumir_ingredientes(receita_excessiva, None)

print("\n\n12. Estoque — latas")
coca1 = BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350)
coca2 = BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350)
guarana = BebidaLata("Guaraná", preco=5.5, marca="Antarctica", volume_ml=350)

estoque.reabastecer_latas("Coca-Cola", [coca1, coca2])
estoque.reabastecer_latas("Guaraná", [guarana])

print("\n12.1 tem_lata (com e sem estoque)")
print(f"Tem Coca-Cola? {estoque.tem_lata('Coca-Cola')}")
print(f"Tem Pepsi (nunca cadastrada)? {estoque.tem_lata('Pepsi')}")

print("\n12.2 retirar_lata até esvaziar")
retirada = estoque.retirar_lata("Coca-Cola")
print(f"Retirada: {retirada.get_nome()} ({retirada.get_preco()})")
estoque.retirar_lata("Coca-Cola")

print("\n12.3 retirar_lata com estoque vazio")
estoque.retirar_lata("Coca-Cola")

print("\n\n13. BebidaLata.preparar() — fluxo completo")
coca3 = BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350)
estoque.reabastecer_latas("Coca-Cola", [coca3])

dispensador_coca = DispensadorLata("Coca-Cola", estoque)
dispensador_guarana = DispensadorLata("Guaraná", estoque)
dispensadores_latas = [dispensador_coca, dispensador_guarana]

print("\n13.1 OK — consome do estoque")
coca3.preparar(dispensadores_latas)

print("\n13.2 Sem estoque — Coca-Cola já zerada")
coca3.preparar(dispensadores_latas)

print("\n13.3 Sem dispensador correspondente")
sukita = BebidaLata("Sukita", preco=5.0, marca="Sukita", volume_ml=350)
sukita.preparar(dispensadores_latas)

print("\n\n14. Estado final do Estoque")
print(estoque)
