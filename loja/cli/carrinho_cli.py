# loja/cli/carrinho_cli.py
import typer
from typing import Optional

from loja import services

app = typer.Typer(help="Comandos para manipular o carrinho de compras.")


@app.command("mostrar")
def mostrar_carrinho(
    cliente_id: int = typer.Argument(..., help="ID do cliente"),
):
    """
    Mostra o carrinho atual do cliente.
    """
    carrinho = services.obter_carrinho_ativo(cliente_id)

    if not carrinho or not carrinho.itens:
        typer.echo("Carrinho vazio.")
        raise typer.Exit()

    typer.echo(f"Carrinho ID: {carrinho.id}")
    typer.echo(f"Cliente: {carrinho.cliente.nome}")
    typer.echo("Itens:")
    for item in carrinho.itens:
        typer.echo(
            f"- {item.produto.nome} (SKU {item.produto.sku}) "
            f"x {item.quantidade} = R${item.subtotal:.2f}"
        )
    typer.echo(f"Subtotal: R${carrinho.subtotal:.2f}")


@app.command("adicionar-item")
def adicionar_item(
    cliente_id: int = typer.Argument(..., help="ID do cliente"),
    sku: int = typer.Argument(..., help="SKU do produto"),
    quantidade: int = typer.Argument(..., help="Quantidade"),
):
    """
    Adiciona um item ao carrinho do cliente.
    """
    carrinho = services.adicionar_item_carrinho(
        cliente_id=cliente_id, sku=sku, quantidade=quantidade
    )
    typer.echo(
        f"✅ Item adicionado ao carrinho {carrinho.id}. Subtotal: R${carrinho.subtotal:.2f}"
    )


@app.command("remover-item")
def remover_item(
    cliente_id: int = typer.Argument(..., help="ID do cliente"),
    sku: int = typer.Argument(..., help="SKU do produto a remover"),
):
    """
    Remove um item do carrinho.
    """
    carrinho = services.remover_item_carrinho(cliente_id=cliente_id, sku=sku)
    typer.echo(
        f"✅ Item removido. Subtotal atual do carrinho {carrinho.id}: R${carrinho.subtotal:.2f}"
    )


@app.command("alterar-quantidade")
def alterar_quantidade(
    cliente_id: int = typer.Argument(..., help="ID do cliente"),
    sku: int = typer.Argument(..., help="SKU do produto"),
    quantidade: int = typer.Argument(..., help="Nova quantidade"),
):
    """
    Altera a quantidade de um item no carrinho.
    """
    carrinho = services.alterar_quantidade_item_carrinho(
        cliente_id=cliente_id, sku=sku, quantidade=quantidade
    )
    typer.echo(
        f"✅ Quantidade atualizada. Subtotal do carrinho {carrinho.id}: R${carrinho.subtotal:.2f}"
    )
