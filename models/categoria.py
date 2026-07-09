"""
Model: Categoria

Representa um setor da loja (ex.: Hortifruti, Açougue...). Cada categoria
agrupa produtos e tem um código de setor exibido no chão de loja.
"""

from models.database import get_connection


class Categoria:
    def __init__(self, id=None, nome="", codigo_setor="", total_produtos=None):
        self.id = id
        self.nome = nome
        self.codigo_setor = codigo_setor
        self.total_produtos = total_produtos

    @staticmethod
    def _from_row(row):
        return Categoria(
            id=row["id"],
            nome=row["nome"],
            codigo_setor=row["codigo_setor"],
            total_produtos=row["total_produtos"] if "total_produtos" in row.keys() else None,
        )

    @classmethod
    def listar_todas(cls):
        """Retorna todas as categorias, com a contagem de produtos de cada uma."""
        conn = get_connection()
        rows = conn.execute(
            """
            SELECT categorias.*, COUNT(produtos.id) AS total_produtos
            FROM categorias
            LEFT JOIN produtos ON produtos.categoria_id = categorias.id
            GROUP BY categorias.id
            ORDER BY categorias.nome
            """
        ).fetchall()
        conn.close()
        return [cls._from_row(row) for row in rows]

    @classmethod
    def buscar_por_id(cls, categoria_id):
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM categorias WHERE id = ?", (categoria_id,)
        ).fetchone()
        conn.close()
        return cls._from_row(row) if row else None

    def salvar(self):
        """Insere (se for nova) ou atualiza (se já tiver id) a categoria."""
        conn = get_connection()
        if self.id is None:
            cursor = conn.execute(
                "INSERT INTO categorias (nome, codigo_setor) VALUES (?, ?)",
                (self.nome, self.codigo_setor),
            )
            self.id = cursor.lastrowid
        else:
            conn.execute(
                "UPDATE categorias SET nome = ?, codigo_setor = ? WHERE id = ?",
                (self.nome, self.codigo_setor, self.id),
            )
        conn.commit()
        conn.close()
        return self

    def excluir(self):
        conn = get_connection()
        conn.execute("DELETE FROM categorias WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()
