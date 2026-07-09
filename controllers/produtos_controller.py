"""
Controller: Produtos

Rotas de gestão dos produtos do estoque: listar, criar, editar, excluir.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

from models.produto import Produto
from models.categoria import Categoria

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")


def _ler_dados_do_formulario(form):
    """Converte e valida os dados vindos do form. Retorna (dados, erro)."""
    nome = form.get("nome", "").strip()
    categoria_id = form.get("categoria_id") or None

    try:
        preco = float(form.get("preco", "").replace(",", "."))
    except ValueError:
        return None, "Informe um preço válido."

    try:
        quantidade = int(form.get("quantidade", ""))
    except ValueError:
        return None, "Informe uma quantidade válida."

    if not nome:
        return None, "Informe o nome do produto."
    if preco < 0 or quantidade < 0:
        return None, "Preço e quantidade não podem ser negativos."

    return {
        "nome": nome,
        "preco": preco,
        "quantidade": quantidade,
        "categoria_id": int(categoria_id) if categoria_id else None,
    }, None


@produtos_bp.route("/")
def listar():
    produtos = Produto.listar_todos()
    return render_template("produtos/lista.html", produtos=produtos)


@produtos_bp.route("/novo", methods=["GET", "POST"])
def novo():
    categorias = Categoria.listar_todas()

    if request.method == "POST":
        dados, erro = _ler_dados_do_formulario(request.form)
        if erro:
            flash(erro, "erro")
            return render_template("produtos/form.html", produto=None, categorias=categorias)

        produto = Produto(**dados)
        produto.salvar()
        flash(f'Produto "{produto.nome}" criado com sucesso.', "sucesso")
        return redirect(url_for("produtos.listar"))

    return render_template("produtos/form.html", produto=None, categorias=categorias)


@produtos_bp.route("/<int:produto_id>/editar", methods=["GET", "POST"])
def editar(produto_id):
    produto = Produto.buscar_por_id(produto_id)
    if produto is None:
        flash("Produto não encontrado.", "erro")
        return redirect(url_for("produtos.listar"))

    categorias = Categoria.listar_todas()

    if request.method == "POST":
        dados, erro = _ler_dados_do_formulario(request.form)
        if erro:
            flash(erro, "erro")
            return render_template("produtos/form.html", produto=produto, categorias=categorias)

        produto.nome = dados["nome"]
        produto.preco = dados["preco"]
        produto.quantidade = dados["quantidade"]
        produto.categoria_id = dados["categoria_id"]
        produto.salvar()
        flash(f'Produto "{produto.nome}" atualizado com sucesso.', "sucesso")
        return redirect(url_for("produtos.listar"))

    return render_template("produtos/form.html", produto=produto, categorias=categorias)


@produtos_bp.route("/<int:produto_id>/excluir", methods=["POST"])
def excluir(produto_id):
    produto = Produto.buscar_por_id(produto_id)
    if produto is not None:
        produto.excluir()
        flash(f'Produto "{produto.nome}" excluído.', "sucesso")
    return redirect(url_for("produtos.listar"))
