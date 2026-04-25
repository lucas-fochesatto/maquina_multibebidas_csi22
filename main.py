from bebidas.bebida_dosada import BebidaDosada
from bebidas.ingrediente import Ingrediente
from bebidas.receita import Receita
from dispensadores.dispensador_ingrediente import DispensadorIngrediente

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
