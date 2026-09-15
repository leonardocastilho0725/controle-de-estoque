# Controle de Estoque

Sistema de linha de comando para gerenciar o estoque de produtos, desenvolvido em Python com **Programação Orientada a Objetos** e **banco de dados SQLite**.

## Funcionalidades

- Cadastrar produtos (nome, preço, quantidade inicial e estoque mínimo)
- Dar entrada de estoque
- Dar saída de estoque (com validação — não permite retirar mais do que há disponível)
- Relatório com todos os produtos cadastrados e valor total em estoque
- Alerta de produtos com estoque abaixo do mínimo definido
- Histórico de movimentações (entradas e saídas) salvo no banco de dados

## Tecnologias e conceitos utilizados

- **Python 3**
- **Programação Orientada a Objetos**: classe `Produto`, com atributos e métodos próprios (`dar_entrada`, `dar_saida`, `esta_em_falta`)
- **SQLite** (`sqlite3`) para persistência de dados, com tabelas `produtos` e `movimentacoes`
- Separação de responsabilidades: `produto.py` (regra de negócio), `banco.py` (acesso a dados) e `main.py` (interface/menu)
- Tratamento de erros com `try`/`except`

## Estrutura do projeto

```
controle_estoque/
├── main.py       # Menu e ponto de entrada do programa
├── produto.py    # Classe Produto (POO)
├── banco.py      # Classe EstoqueDB — acesso ao SQLite
└── estoque.db    # Criado automaticamente na primeira execução
```

## Como executar

```bash
python3 main.py
```

Na primeira execução, o programa cria automaticamente o arquivo `estoque.db` com as tabelas necessárias.

## Menu do sistema

```
1 - Cadastrar produto
2 - Dar entrada de estoque
3 - Dar saída de estoque
4 - Relatório de produtos
5 - Alertar estoque baixo
0 - Encerrar o sistema
```

## Próximos passos

- [ ] Edição de produtos já cadastrados
- [ ] Consulta ao histórico de movimentações por produto
- [ ] Filtro de relatório por categoria

## Autor

Leonardo Castilho — estudante de Análise e Desenvolvimento de Sistemas
