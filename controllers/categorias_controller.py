"""
Controller: Categorias

Rotas de gestão das categorias (setores da loja): listar, criar, editar,
excluir.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash

from models.categoria import Categoria

categorias_bp = Blueprint("categorias", __name__, url_prefix="/categorias")


@categorias_bp.route("/")
def listar():
    categorias = Categoria.listar_todas()
    return render_template("categorias/lista.html", categorias=categorias)


@categorias_bp.route("/nova", methods=["GET", "POST"])
def nova():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        codigo_setor = request.form.get("codigo_setor", "").strip().upper()

        if not nome or not codigo_setor:
            flash("Preencha nome e código do setor.", "erro")
            return render_template("categorias/form.html", categoria=None)

        categoria = Categoria(nome=nome, codigo_setor=codigo_setor)
        categoria.salvar()
        flash(f'Categoria "{categoria.nome}" criada com sucesso.', "sucesso")
        return redirect(url_for("categorias.listar"))

    return render_template("categorias/form.html", categoria=None)


@categorias_bp.route("/<int:categoria_id>/editar", methods=["GET", "POST"])
def editar(categoria_id):
    categoria = Categoria.buscar_por_id(categoria_id)
    if categoria is None:
        flash("Categoria não encontrada.", "erro")
        return redirect(url_for("categorias.listar"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        codigo_setor = request.form.get("codigo_setor", "").strip().upper()

        if not nome or not codigo_setor:
            flash("Preencha nome e código do setor.", "erro")
            return render_template("categorias/form.html", categoria=categoria)

        categoria.nome = nome
        categoria.codigo_setor = codigo_setor
        categoria.salvar()
        flash(f'Categoria "{categoria.nome}" atualizada com sucesso.', "sucesso")
        return redirect(url_for("categorias.listar"))

    return render_template("categorias/form.html", categoria=categoria)


@categorias_bp.route("/<int:categoria_id>/excluir", methods=["POST"])
def excluir(categoria_id):
    categoria = Categoria.buscar_por_id(categoria_id)
    if categoria is not None:
        categoria.excluir()
        flash(f'Categoria "{categoria.nome}" excluída.', "sucesso")
    return redirect(url_for("categorias.listar"))
