"""
Camada de acesso ao banco de dados (SQLite).

O banco fica em instance/estoque.db — essa pasta já é ignorada pelo git
(.gitignore), então cada máquina gera o próprio banco ao rodar o projeto.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "instance" / "estoque.db"


def get_connection():
    """Abre uma conexão nova com o banco, criando a pasta se necessário."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Cria as tabelas caso ainda não existam."""
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS categorias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo_setor TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            preco REAL NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0,
            categoria_id INTEGER,
            FOREIGN KEY (categoria_id) REFERENCES categorias (id) ON DELETE SET NULL
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    """Popula o banco com dados de exemplo, só na primeira vez (tabelas vazias)."""
    conn = get_connection()
    total_categorias = conn.execute("SELECT COUNT(*) FROM categorias").fetchone()[0]

    if total_categorias == 0:
        categorias = [
            ("Hortifruti", "A1"),
            ("Açougue e peixaria", "A2"),
            ("Padaria", "A3"),
            ("Mercearia", "A4"),
            ("Frios e laticínios", "A5"),
            ("Bebidas", "A6"),
            ("Higiene e limpeza", "A7"),
            ("Bazar", "A8"),
        ]
        conn.executemany(
            "INSERT INTO categorias (nome, codigo_setor) VALUES (?, ?)", categorias
        )
        conn.commit()

        ids = {
            row["nome"]: row["id"]
            for row in conn.execute("SELECT id, nome FROM categorias").fetchall()
        }

        produtos = [
            ("Tomate", 4.99, 120, ids["Hortifruti"]),
            ("Picanha bovina (kg)", 39.90, 8, ids["Açougue e peixaria"]),
            ("Pão francês (kg)", 0.90, 200, ids["Padaria"]),
            ("Arroz branco 5kg", 24.90, 60, ids["Mercearia"]),
            ("Queijo mussarela (kg)", 32.50, 15, ids["Frios e laticínios"]),
            ("Refrigerante 2L", 7.99, 5, ids["Bebidas"]),
            ("Sabão em pó 1,6kg", 18.90, 40, ids["Higiene e limpeza"]),
            ("Balde plástico 10L", 12.90, 25, ids["Bazar"]),
        ]
        conn.executemany(
            """INSERT INTO produtos (nome, preco, quantidade, categoria_id)
               VALUES (?, ?, ?, ?)""",
            produtos,
        )
        conn.commit()

    conn.close()
