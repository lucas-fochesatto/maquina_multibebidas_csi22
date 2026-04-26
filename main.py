from bebidas.bebida_dosada import BebidaDosada
from bebidas.bebida_lata import BebidaLata
from bebidas.ingrediente import Ingrediente
from bebidas.receita import Receita
from core.estoque import Estoque
from core.gerenciador import Gerenciador
from core.maquina import MaquinaCafeMB
from core.venda import Venda
from dispensadores.dispensador_ingrediente import DispensadorIngrediente
from dispensadores.dispensador_lata import DispensadorLata
from pagamentos.cartao_credito import CartaoCredito
from pagamentos.cartao_debito import CartaoDebito
from pagamentos.pix import Pix

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

print("\n\n15. Pagamentos — Pix, Cartão de Crédito, Cartão de Débito")

print("\n15.1 Pix")
pix_demo = Pix(8.0, "caixa@cafe.com")
print(f"Valor: R$ {pix_demo.get_valor():.2f} | Chave: {pix_demo.get_chave_destino()}")
print(f"Aprovado antes de processar? {pix_demo.get_aprovado()}")
pix_demo.processar()
print(f"Aprovado depois de processar? {pix_demo.get_aprovado()}")

print("\n15.2 Cartão de Crédito")
credito_demo = CartaoCredito(15.0, "1111-2222-3333-4444", "Lucas Fochesatto", "12/30", "123")
print(f"Titular: {credito_demo.get_titular()} | Valor: R$ {credito_demo.get_valor():.2f}")
credito_demo.processar()

print("\n15.3 Cartão de Débito")
debito_demo = CartaoDebito(12.0, "5555-6666-7777-8888", "Lucas Fochesatto", "12/30", "456")
print(f"Titular: {debito_demo.get_titular()} | Valor: R$ {debito_demo.get_valor():.2f}")
debito_demo.processar()


print("\n\n16. Venda — registro de transação + comprovante")

cafe_v = Ingrediente("Café", quantidade=200, capacidade_maxima=500, porcao_padrao=10.0)
leite_v = Ingrediente("Leite", quantidade=300, capacidade_maxima=500, porcao_padrao=20.0)
cappuccino_v = BebidaDosada("Cappuccino", preco=8.0, receita=Receita({cafe_v: 100, leite_v: 70}))

print("\n16.1 Criar Venda (Venda.__init__ processa o pagamento)")
venda_demo = Venda(cappuccino_v, Pix(8.0, "caixa@cafe.com"))
print(f"Status: {venda_demo.get_status()}")
print(f"Bebida vendida: {venda_demo.get_bebida().get_nome()}")
print(f"Data: {venda_demo.get_data().strftime('%d/%m/%Y %H:%M:%S')}")

print("\n16.2 Comprovante")
print(venda_demo.comprovante())


print("\n\n17. Gerenciador — relatório financeiro")
gerenciador_demo = Gerenciador()

print("\n17.1 Estado inicial")
print(gerenciador_demo.relatorio())

print("\n17.2 Registrando 2 dosadas + 1 lata")
coca_v = BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350)
gerenciador_demo.registrar_venda(Venda(cappuccino_v, Pix(8.0, "caixa@cafe.com")))
gerenciador_demo.registrar_venda(Venda(cappuccino_v, CartaoCredito(8.0, "1234", "Lucas", "12/30", "111")))
gerenciador_demo.registrar_venda(Venda(coca_v, Pix(6.0, "caixa@cafe.com")))

print("\n17.3 Relatório após 3 vendas")
for chave, valor in gerenciador_demo.relatorio().items():
    print(f"  {chave}: {valor}")
print(f"  histórico: {len(gerenciador_demo.get_historico_vendas())} vendas")


print("\n\n18. MaquinaCafeMB — ligar / desligar / limpar")

estoque_m = Estoque()
gerenciador_m = Gerenciador()
cafe_m = Ingrediente("Café", quantidade=500, capacidade_maxima=1000, porcao_padrao=10.0)
leite_m = Ingrediente("Leite", quantidade=500, capacidade_maxima=1000, porcao_padrao=20.0)
estoque_m.cadastrar_ingrediente(cafe_m)
estoque_m.cadastrar_ingrediente(leite_m)
estoque_m.reabastecer_copos(10)

dispensadores_m = [
    DispensadorIngrediente(cafe_m),
    DispensadorIngrediente(leite_m),
    DispensadorLata("Coca-Cola", estoque_m),
]

maquina = MaquinaCafeMB(estoque_m, gerenciador_m, dispensadores_m)

print("\n18.1 Tentar usar com máquina desligada")
maquina.consultar_bebidas()
maquina.limpar()

print("\n18.2 Ligar (e tentar ligar de novo)")
maquina.ligar()
maquina.ligar()

print("\n18.3 Desligar (e tentar desligar de novo) e religar")
maquina.desligar()
maquina.desligar()
maquina.ligar()

print("\n18.4 Limpar")
maquina.limpar()


print("\n\n19. MaquinaCafeMB — cardápio (autenticação obrigatória)")
print("    >>> use Login: admin / Senha: ita2026 <<<")

cappuccino_m = BebidaDosada("Cappuccino", preco=8.0, receita=Receita({cafe_m: 100, leite_m: 70}))
coca_m = BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350)
estoque_m.reabastecer_latas("Coca-Cola", [
    BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350),
    BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350),
])

print("\n19.1 adicionar_bebida (Cappuccino) — vai pedir login/senha")
maquina.adicionar_bebida(cappuccino_m)

print("\n19.2 adicionar_bebida (Coca-Cola) — vai pedir login/senha")
maquina.adicionar_bebida(coca_m)

print("\n19.3 Cardápio atualizado")
maquina.consultar_bebidas()


print("\n\n20. fazer_bebida — sucesso e casos de erro")

print("\n20.1 Dosada (cappuccino) — OK")
maquina.fazer_bebida(cappuccino_m, None)

print("\n20.2 Lata (coca) — OK")
maquina.fazer_bebida(coca_m, None)

print("\n20.3 Esvaziar estoque de Coca e tentar de novo")
maquina.fazer_bebida(coca_m, None)
print("\n  → próxima tentativa deve falhar:")
maquina.fazer_bebida(coca_m, None)

print("\n20.4 Esgotar copos e tentar dosada")
while estoque_m.tem_copo():
    estoque_m.consumir_copo()
maquina.fazer_bebida(cappuccino_m, None)

print("\n20.5 Reabastecer copos e forçar máquina suja")
estoque_m.reabastecer_copos(5)
maquina._MaquinaCafeMB__nivel_limpeza = 0  # gambi pontual: forçar nível 0 sem rodar 10 ciclos
maquina.fazer_bebida(cappuccino_m, None)

print("\n20.6 Limpar e tentar novamente")
maquina.limpar()
maquina.fazer_bebida(cappuccino_m, None)

print("\n20.7 Máquina desligada")
maquina.desligar()
maquina.fazer_bebida(cappuccino_m, None)
maquina.ligar()


print("\n\n21. Venda end-to-end via MaquinaCafeMB")

estoque_m.reabastecer_latas("Coca-Cola", [
    BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350),
    BebidaLata("Coca-Cola", preco=6.0, marca="Coca", volume_ml=350),
])

print("\n21.1 Cappuccino com Pix")
v = maquina.venda(cappuccino_m, Pix(8.0, "caixa@cafe.com"), None)
print(f"  Retorno: status={v.get_status()}" if v else "  Retorno: None")

print("\n21.2 Coca com Cartão de Crédito")
v = maquina.venda(coca_m, CartaoCredito(6.0, "1111-2222-3333-4444", "Lucas", "12/30", "123"), None)
print(f"  Retorno: status={v.get_status()}" if v else "  Retorno: None")

print("\n21.3 Bebida fora do cardápio")
expresso = BebidaDosada("Expresso", preco=5.0, receita=Receita({cafe_m: 100}))
v = maquina.venda(expresso, Pix(5.0, "caixa@cafe.com"), None)
print(f"  Retorno: {v}")


print("\n\n22. Operações administrativas (autenticação)")
print("    >>> use Login: admin / Senha: ita2026 <<<")

print("\n22.1 ver_estoque_atual — vai pedir login/senha")
maquina.ver_estoque_atual()

print("\n22.2 ver_relatorio — vai pedir login/senha")
maquina.ver_relatorio()
