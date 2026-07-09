"""
Hipermarket Boa Compra - Sistema de Controle de Estoque

Nível 2 (BMVC II): CRUD completo de Produtos e Categorias, com dados
persistidos em SQLite, seguindo a estrutura BMVC da disciplina:

- controllers/  -> rotas/lógica de controle (blueprints do Flask)
- models/       -> classes Python (Categoria, Produto, acesso ao banco)
- views/html/   -> páginas HTML (Jinja2)
- static/       -> CSS, JS e imagens
"""

from flask import Flask, render_template

from models.database import init_db, seed_db
from controllers.categorias_controller import categorias_bp
from controllers.produtos_controller import produtos_bp

app = Flask(__name__, template_folder="views/html")
app.secret_key = "hipermarket-boa-compra-dev"  # troque por algo seguro em produção

app.register_blueprint(categorias_bp)
app.register_blueprint(produtos_bp)


@app.route("/")
def home():
    """Página institucional do mercado (Nível 1)."""
    return render_template("index.html")


init_db()
seed_db()


if __name__ == "__main__":
    app.run(debug=True)
