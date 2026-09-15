import sqlite3
from datetime import datetime

from produto import Produto


class EstoqueDB:
    


    def __init__(self, caminho="estoque.db"):
        self.conexao = sqlite3.connect(caminho)
        self.conexao.row_factory = sqlite3.Row 
        self._criar_tabelas()

    def _criar_tabelas(self):
        cursor = self.conexao.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                estoque_minimo INTEGER NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                produto_id INTEGER NOT NULL,
                tipo TEXT NOT NULL,
                quantidade INTEGER NOT NULL,
                data TEXT NOT NULL,
                FOREIGN KEY (produto_id) REFERENCES produtos (id)
            )
            """
        )
        self.conexao.commit()

    
    def inserir_produto(self, produto):
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, preco, quantidade, estoque_minimo) VALUES (?, ?, ?, ?)",
            (produto.nome, produto.preco, produto.quantidade, produto.estoque_minimo),
        )
        self.conexao.commit()
        produto.id = cursor.lastrowid
        return produto

    def registrar_movimentacao(self, produto_id, tipo, quantidade):
        cursor = self.conexao.cursor()
        cursor.execute(
            "INSERT INTO movimentacoes (produto_id, tipo, quantidade, data) VALUES (?, ?, ?, ?)",
            (produto_id, tipo, quantidade, datetime.now().strftime("%Y-%m-%d %H:%M")),
        )
        self.conexao.commit()

    # ---------- READ ----------
    def listar_produtos(self):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM produtos ORDER BY nome")
        return [self._linha_para_produto(linha) for linha in cursor.fetchall()]

    def buscar_produto_por_id(self, produto_id):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        linha = cursor.fetchone()
        return self._linha_para_produto(linha) if linha else None

    def buscar_produtos_por_nome(self, nome):
        cursor = self.conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{nome}%",))
        return [self._linha_para_produto(linha) for linha in cursor.fetchall()]

    def produtos_em_falta(self):
        return [p for p in self.listar_produtos() if p.esta_em_falta()]

    # ---------- UPDATE ----------
    def atualizar_quantidade(self, produto):
        cursor = self.conexao.cursor()
        cursor.execute(
            "UPDATE produtos SET quantidade = ? WHERE id = ?",
            (produto.quantidade, produto.id),
        )
        self.conexao.commit()

    # ---------- DELETE ----------
    def remover_produto(self, produto_id):
        cursor = self.conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        self.conexao.commit()
        return cursor.rowcount > 0

    # ---------- Auxiliar ----------
    def _linha_para_produto(self, linha):
        return Produto(
            id=linha["id"],
            nome=linha["nome"],
            preco=linha["preco"],
            quantidade=linha["quantidade"],
            estoque_minimo=linha["estoque_minimo"],
        )

    def fechar(self):
        self.conexao.close()
