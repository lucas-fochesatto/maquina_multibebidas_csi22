from bebidas.bebida_dosada import BebidaDosada
from bebidas.bebida_lata import BebidaLata
from bebidas.ingrediente import Ingrediente
from bebidas.receita import Receita
from pagamentos.cartao_credito import CartaoCredito
from pagamentos.cartao_debito import CartaoDebito
from pagamentos.pix import Pix
from seed import criar_maquina_populada


def ler_int(prompt, minimo=None, maximo=None):
    while True:
        entrada = input(prompt).strip()
        try:
            valor = int(entrada)
        except ValueError:
            print("  → Digite um número inteiro.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  → Valor deve ser >= {minimo}.")
            continue
        if maximo is not None and valor > maximo:
            print(f"  → Valor deve ser <= {maximo}.")
            continue
        return valor


def ler_float(prompt, minimo=None):
    while True:
        entrada = input(prompt).strip().replace(",", ".")
        try:
            valor = float(entrada)
        except ValueError:
            print("  → Digite um número.")
            continue
        if minimo is not None and valor < minimo:
            print(f"  → Valor deve ser >= {minimo}.")
            continue
        return valor


def escolher_bebida(maquina):
    bebidas = maquina.get_bebidas_disponiveis()
    if not bebidas:
        print("Cardápio vazio.")
        return None

    print("\n--- Escolha uma bebida ---")
    for i, b in enumerate(bebidas, 1):
        tipo = "dosada" if isinstance(b, BebidaDosada) else "lata"
        print(f"  {i}. {b.get_nome():<20} R$ {b.get_preco():.2f}  ({tipo})")
    print("  0. Voltar")

    escolha = ler_int("Bebida: ", minimo=0, maximo=len(bebidas))
    if escolha == 0:
        return None
    return bebidas[escolha - 1]


def escolher_doses(bebida):
    if not isinstance(bebida, BebidaDosada):
        return None

    resp = input("\nQuer customizar as doses? (s/N): ").strip().lower()
    if resp != "s":
        return None

    doses = {}
    print("Para cada ingrediente, escolha um percentual válido: 30, 50, 70 ou 100.")
    print("Pressione ENTER para manter o padrão da receita.")

    for ingrediente in bebida.get_receita().get_ingredientes():
        while True:
            entrada = input(f"  {ingrediente.get_nome()} (%): ").strip()
            if entrada == "":
                break
            try:
                pct = int(entrada)
            except ValueError:
                print("    → Digite 30, 50, 70 ou 100.")
                continue
            if pct not in (30, 50, 70, 100):
                print("    → Apenas 30, 50, 70 ou 100 são aceitos.")
                continue
            doses[ingrediente] = pct
            break

    return doses if doses else None


def escolher_pagamento(valor):
    print("\n--- Forma de pagamento ---")
    print("  1. Pix")
    print("  2. Cartão de Crédito")
    print("  3. Cartão de Débito")
    print("  0. Cancelar")

    opcao = ler_int("Forma: ", minimo=0, maximo=3)

    if opcao == 0:
        return None
    if opcao == 1:
        chave = input("Chave Pix de destino: ").strip() or "caixa@cafe.com"
        return Pix(valor, chave)

    print("(Dados do cartão — pode usar valores fictícios)")
    numero = input("Número: ").strip() or "1111-2222-3333-4444"
    titular = input("Titular: ").strip() or "Cliente"
    validade = input("Validade (MM/AA): ").strip() or "12/30"
    cvv = input("CVV: ").strip() or "123"

    if opcao == 2:
        return CartaoCredito(valor, numero, titular, validade, cvv)
    return CartaoDebito(valor, numero, titular, validade, cvv)


def comprar_bebida(maquina, ultima_venda_ref):
    bebida = escolher_bebida(maquina)
    if bebida is None:
        return

    doses = escolher_doses(bebida)
    pagamento = escolher_pagamento(bebida.get_preco())
    if pagamento is None:
        print("Compra cancelada.")
        return

    venda = maquina.venda(bebida, pagamento, doses)
    if venda is not None and venda.get_status() == "concluida":
        ultima_venda_ref["venda"] = venda
        print(venda.comprovante())


def alternar_ligado(maquina):
    if maquina.esta_ligada():
        maquina.desligar()
    else:
        maquina.ligar()


def reabastecer_ingrediente(maquina):
    nome = input("Nome do ingrediente: ").strip()
    if not nome:
        print("Operação cancelada.")
        return
    quantidade = ler_float("Quantidade (g): ", minimo=0)
    maquina.atualizar_ingrediente(nome, quantidade)


def reabastecer_copos(maquina):
    quantidade = ler_int("Quantidade de copos: ", minimo=1)
    maquina.atualizar_copos(quantidade)


def reabastecer_latas(maquina):
    nome = input("Tipo da lata (ex: Coca-Cola): ").strip()
    if not nome:
        print("Operação cancelada.")
        return
    quantidade = ler_int("Quantidade de latas: ", minimo=1)
    marca = input("Marca: ").strip() or nome
    volume = ler_int("Volume (ml): ", minimo=1)
    preco = ler_float("Preço (R$): ", minimo=0)

    latas = [BebidaLata(nome, preco=preco, marca=marca, volume_ml=volume) for _ in range(quantidade)]
    maquina.atualizar_estoque_latas(nome, latas)


def adicionar_bebida_cardapio(maquina):
    print("\nTipo de bebida:")
    print("  1. Lata (já existente no estoque)")
    print("  2. Dosada (nova receita)")
    tipo = ler_int("Tipo: ", minimo=1, maximo=2)

    if tipo == 1:
        nome = input("Nome da lata: ").strip()
        marca = input("Marca: ").strip() or nome
        volume = ler_int("Volume (ml): ", minimo=1)
        preco = ler_float("Preço (R$): ", minimo=0)
        bebida = BebidaLata(nome, preco=preco, marca=marca, volume_ml=volume)
    else:
        nome = input("Nome da bebida dosada: ").strip()
        preco = ler_float("Preço (R$): ", minimo=0)
        ingredientes_estoque = maquina.listar_ingredientes()
        if not ingredientes_estoque:
            print("Não há ingredientes cadastrados no estoque.")
            return

        print("\nIngredientes disponíveis no estoque:")
        nomes = list(ingredientes_estoque.keys())
        for i, n in enumerate(nomes, 1):
            print(f"  {i}. {n}")
        print("Informe o índice de cada ingrediente (vazio para finalizar).")

        receita_ingredientes = {}
        while True:
            entrada = input("Índice do ingrediente: ").strip()
            if entrada == "":
                break
            try:
                idx = int(entrada)
            except ValueError:
                print("  → Digite um número.")
                continue
            if not (1 <= idx <= len(nomes)):
                print(f"  → Índice deve estar entre 1 e {len(nomes)}.")
                continue
            ingrediente = ingredientes_estoque[nomes[idx - 1]]
            pct = ler_int(f"  Percentual padrão (30/50/70/100): ")
            if pct not in (30, 50, 70, 100):
                print("  → Apenas 30, 50, 70 ou 100 são aceitos.")
                continue
            receita_ingredientes[ingrediente] = pct

        if not receita_ingredientes:
            print("Receita vazia. Operação cancelada.")
            return

        bebida = BebidaDosada(nome, preco=preco, receita=Receita(receita_ingredientes))

    maquina.adicionar_bebida(bebida)


def menu_principal():
    print("\n" + "=" * 40)
    print("       MÁQUINA DE CAFÉ MB")
    print("=" * 40)
    print("  1. Ver cardápio")
    print("  2. Comprar bebida")
    print("  3. Ver comprovante da última venda")
    print("  4. Ligar / desligar máquina")
    print("  5. Limpar máquina")
    print("  --- ADMIN (login: admin / senha: ita2026) ---")
    print("  6. Ver estoque")
    print("  7. Reabastecer ingrediente")
    print("  8. Reabastecer copos")
    print("  9. Reabastecer latas")
    print("  10. Adicionar bebida ao cardápio")
    print("  11. Ver relatório financeiro")
    print("  0. Sair")
    return ler_int("Opção: ", minimo=0, maximo=11)


def main():
    print("Inicializando máquina...\n")
    maquina = criar_maquina_populada()
    ultima_venda_ref = {"venda": None}

    while True:
        opcao = menu_principal()

        if opcao == 0:
            print("\nAté logo!")
            break
        elif opcao == 1:
            maquina.consultar_bebidas()
        elif opcao == 2:
            comprar_bebida(maquina, ultima_venda_ref)
        elif opcao == 3:
            venda = ultima_venda_ref["venda"]
            if venda is None:
                print("Nenhuma venda registrada nesta sessão.")
            else:
                print(venda.comprovante())
        elif opcao == 4:
            alternar_ligado(maquina)
        elif opcao == 5:
            maquina.limpar()
        elif opcao == 6:
            maquina.ver_estoque_atual()
        elif opcao == 7:
            reabastecer_ingrediente(maquina)
        elif opcao == 8:
            reabastecer_copos(maquina)
        elif opcao == 9:
            reabastecer_latas(maquina)
        elif opcao == 10:
            adicionar_bebida_cardapio(maquina)
        elif opcao == 11:
            maquina.ver_relatorio()


if __name__ == "__main__":
    main()
