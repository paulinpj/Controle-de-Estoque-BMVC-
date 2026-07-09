"""
Model: Produto

Representa um item de estoque. Cada produto pertence a uma categoria
(setor da loja) e guarda preço e quantidade disponível.
"""

from models.database import get_connection

LIMITE_ESTOQUE_BAIXO = 10


class Produto:
    def __init__(self, id=None, nome="", preco=0.0, quantidade=0,
                 categoria_id=None, categoria_nome=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.categoria_id = categoria_id
        self.categoria_nome = categoria_nome

    @staticmethod
    def _from_row(row):
        return Produto(
            id=row["id"],
            nome=row["nome"],
            preco=row["preco"],
            quantidade=row["quantidade"],
            categoria_id=row["categoria_id"],
            categoria_nome=row["categoria_nome"] if "categoria_nome" in row.keys() else None,
        )

    @property
    def estoque_baixo(self):
        """Usado hoje para destacar o item na listagem; vira alerta em tempo
        real no Nível 4 (WebSocket)."""
        return self.quantidade <= LIMITE_ESTOQUE_BAIXO

    @classmethod
    def listar_todos(cls):
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT produtos.*, categorias.nome AS categoria_nome
            FROM produtos
            LEFT JOIN categorias ON categorias.id = produtos.categoria_id
            ORDER BY produtos.nome
            """
        ).fetchall()
        conn.close()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def buscar_por_id(cls, produto_id):
        conn = get_connection()
        row = conn.execute(
            """
            SELECT produtos.*, categorias.nome AS categoria_nome
            FROM produtos
            LEFT JOIN categorias ON categorias.id = produtos.categoria_id
            WHERE produtos.id = ?
            """,
            (produto_id,),
        ).fetchone()
        conn.close()
        return cls._from_row(row) if row else None

    def salvar(self):
        """Insere (se for novo) ou atualiza (se já tiver id) o produto."""
        conn = get_connection()
        if self.id is None:
            cursor = conn.execute(
                """INSERT INTO produtos (nome, preco, quantidade, categoria_id)
                   VALUES (?, ?, ?, ?)""",
                (self.nome, self.preco, self.quantidade, self.categoria_id),
            )
            self.id = cursor.lastrowid
        else:
            conn.execute(
                """UPDATE produtos
                   SET nome = ?, preco = ?, quantidade = ?, categoria_id = ?
                   WHERE id = ?""",
                (self.nome, self.preco, self.quantidade, self.categoria_id, self.id),
            )
        conn.commit()
        conn.close()
        return self

    def excluir(self):
        conn = get_connection()
        conn.execute("DELETE FROM produtos WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
