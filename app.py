"""
Hipermarket Boa Compra - Sistema de Controle de Estoque
Nível 1 (BMVC I): página institucional estática.

Estrutura de pastas seguindo o padrão BMVC da disciplina:
- controllers/  -> rotas/lógica de controle (Nível 2+)
- models/       -> classes Python (Produto, Categoria, Usuario...) no Nível 2+
- views/html/   -> páginas HTML (Jinja2)
- static/       -> CSS, JS e imagens
"""

from flask import Flask, render_template

app = Flask(__name__, template_folder="views/html")


@app.route("/")
def home():
    """Página institucional do mercado (Nível 1)."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
