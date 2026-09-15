from banco import EstoqueDB
from produto import Produto

db = EstoqueDB("estoque.db")


# ---------------- Funções auxiliares de entrada ----------------

def ler_inteiro(mensagem, minimo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Erro! O valor deve ser maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Erro! Digite apenas números inteiros.")


def ler_float(mensagem, minimo=None):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
            if minimo is not None and valor < minimo:
                print(f"Erro! O valor deve ser maior ou igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Erro! Digite apenas números (ex: 10.50).")


def ler_texto_nao_vazio(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor == "":
            print("Erro! Esse campo não pode ficar em branco.")
            continue
        return valor


def selecionar_produto():
    """Pede um nome, busca no banco e deixa o usuário escolher entre os resultados."""
    nome_busca = ler_texto_nao_vazio("Digite o nome (ou parte do nome) do produto: ")
    encontrados = db.buscar_produtos_por_nome(nome_busca)

    if not encontrados:
        print("Nenhum produto encontrado com esse nome.")
        return None

    if len(encontrados) == 1:
        return encontrados[0]

    print("Mais de um produto encontrado:")
    for produto in encontrados:
        print(f"  {produto}")
    id_escolhido = ler_inteiro("Digite o ID do produto desejado: ")
    return next((p for p in encontrados if p.id == id_escolhido), None)


# ---------------- Funcionalidades do menu ----------------

def cadastrar_produto():
    print("------- CADASTRAR PRODUTO -------")
    nome = ler_texto_nao_vazio("Nome do produto: ")
    preco = ler_float("Preço (ex: 19.90): ", minimo=0)
    quantidade = ler_inteiro("Quantidade inicial em estoque: ", minimo=0)
    estoque_minimo = ler_inteiro("Estoque mínimo (para alerta): ", minimo=0)

    produto = Produto(nome=nome, preco=preco, quantidade=quantidade, estoque_minimo=estoque_minimo)
    db.inserir_produto(produto)

    if quantidade > 0:
        db.registrar_movimentacao(produto.id, "entrada", quantidade)

    print(f"Produto cadastrado com sucesso! (ID {produto.id})")


def dar_entrada_estoque():
    print("------- ENTRADA DE ESTOQUE -------")
    produto = selecionar_produto()
    if produto is None:
        print("Operação cancelada: produto não encontrado.")
        return

    quantidade = ler_inteiro("Quantidade a adicionar: ", minimo=1)
    produto.dar_entrada(quantidade)
    db.atualizar_quantidade(produto)
    db.registrar_movimentacao(produto.id, "entrada", quantidade)
    print(f"Entrada registrada! Novo estoque de {produto.nome}: {produto.quantidade}")


def dar_saida_estoque():
    print("------- SAÍDA DE ESTOQUE -------")
    produto = selecionar_produto()
    if produto is None:
        print("Operação cancelada: produto não encontrado.")
        return

    quantidade = ler_inteiro("Quantidade a retirar: ", minimo=1)
    try:
        produto.dar_saida(quantidade)
    except ValueError as erro:
        print(f"Erro! {erro}")
        return

    db.atualizar_quantidade(produto)
    db.registrar_movimentacao(produto.id, "saida", quantidade)
    print(f"Saída registrada! Novo estoque de {produto.nome}: {produto.quantidade}")

    if produto.esta_em_falta():
        print(f"Atenção: o estoque de '{produto.nome}' está abaixo do mínimo ({produto.estoque_minimo}).")


def relatorio_produtos():
    print("------- RELATÓRIO DE PRODUTOS -------")
    produtos = db.listar_produtos()
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return

    for produto in produtos:
        print(produto)

    valor_total = sum(p.preco * p.quantidade for p in produtos)
    print("-" * 60)
    print(f"Total de produtos cadastrados: {len(produtos)}")
    print(f"Valor total em estoque: R$ {valor_total:.2f}")


def alertar_estoque_baixo():
    print("------- ALERTA DE ESTOQUE BAIXO -------")
    produtos = db.produtos_em_falta()
    if not produtos:
        print("Nenhum produto está com estoque abaixo do mínimo. Tudo certo!")
        return

    print(f"{len(produtos)} produto(s) com estoque baixo:")
    for produto in produtos:
        print(produto)


# ---------------- Menu principal ----------------

def menu_de_opcoes():
    print("=" * 60)
    print("CONTROLE DE ESTOQUE")
    print("=" * 60)
    print("1 - Cadastrar produto")
    print("2 - Dar entrada de estoque")
    print("3 - Dar saída de estoque")
    print("4 - Relatório de produtos")
    print("5 - Alertar estoque baixo")
    print("0 - Encerrar o sistema")

    while True:
        try:
            return int(input("Escolha uma opção: "))
        except ValueError:
            print("Erro! Digite apenas o número da opção.")


def main():
    print("=" * 60)
    print("BEM VINDO AO CONTROLE DE ESTOQUE")
    print("=" * 60)

    while True:
        opcao = menu_de_opcoes()

        if opcao == 1:
            cadastrar_produto()
        elif opcao == 2:
            dar_entrada_estoque()
        elif opcao == 3:
            dar_saida_estoque()
        elif opcao == 4:
            relatorio_produtos()
        elif opcao == 5:
            alertar_estoque_baixo()
        elif opcao == 0:
            print("Encerrando o programa... até mais!")
            db.fechar()
            break
        else:
            print("Erro! Digite uma opção válida!")


if __name__ == "__main__":
    main()
