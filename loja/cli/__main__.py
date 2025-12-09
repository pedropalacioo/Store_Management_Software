# loja/cli/main.py
import typer

from .produto_cli import app as produto_app
from .cliente_cli import app as cliente_app
from .carrinho_cli import app as carrinho_app
from .pedido_cli import app as pedido_app
from .relatorios_cli import app as relatorio_app

from loja.persistence.db import init_db  # 👈 aqui

app = typer.Typer(help="CLI da Loja Virtual Simplificada")

app.add_typer(produto_app, name="produto")
app.add_typer(cliente_app, name="cliente")
app.add_typer(carrinho_app, name="carrinho")
app.add_typer(pedido_app, name="pedido")
app.add_typer(relatorio_app, name="relatorio")


@app.command("init-db")
def init_db_command():
    """
    Inicializa o banco SQLite (cria tabelas e, se quiser, faz seed).
    """
    init_db()
    typer.echo("✅ Banco SQLite inicializado com sucesso.")


def main():
    app()


if __name__ == "__main__":
    main()


