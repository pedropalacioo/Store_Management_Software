# loja/cli/relatorios_cli.py
import typer
from datetime import date
from typing import Optional

from loja import services

app = typer.Typer(help="Relatórios de vendas e pedidos.")


@app.command("faturamento")
def relatorio_faturamento(
    inicio: date = typer.Option(..., "--inicio", help="Data inicial (YYYY-MM-DD)"),
    fim: date = typer.Option(..., "--fim", help="Data final (YYYY-MM-DD)"),
):
    """
    Relatório de faturamento por período.
    """
    dados = services.relatorio_faturamento_por_periodo(inicio=inicio, fim=fim)

    typer.echo(f"Período: {inicio} a {fim}")
    typer.echo(f"Total faturado: R${dados.total_faturado:.2f}")
    typer.echo(f"Quantidade de pedidos: {dados.qtd_pedidos}")
    typer.echo(f"Ticket médio: R${dados.ticket_medio:.2f}")


@app.command("top-produtos")
def relatorio_top_produtos(
    top_n: int = typer.Option(5, "--top", help="Quantidade de produtos no ranking"),
):
    """
    Top N produtos mais vendidos.
    """
    produtos = services.relatorio_top_produtos(top_n=top_n)

    if not produtos:
        typer.echo("Nenhuma venda registrada.")
        raise typer.Exit()

    typer.echo(f"Top {top_n} produtos mais vendidos:")
    for idx, p in enumerate(produtos, start=1):
        typer.echo(
            f"{idx}. {p['nome']} (SKU {p['sku']}) - qtd vendida: {p['quantidade']} "
            f"- faturamento: R${p['faturamento']:.2f}"
        )


@app.command("vendas-por-uf")
def relatorio_vendas_por_uf():
    """
    Relatório de vendas por UF.
    """
    linhas = services.relatorio_vendas_por_uf()

    if not linhas:
        typer.echo("Nenhuma venda registrada.")
        raise typer.Exit()

    typer.echo("Vendas por UF:")
    for linha in linhas:
        typer.echo(
            f"UF {linha['uf']}: {linha['qtd_pedidos']} pedidos - "
            f"faturamento: R${linha['faturamento']:.2f}"
        )


@app.command("pedidos-por-status")
def relatorio_pedidos_por_status():
    """
    Quantidade e percentual de pedidos por status.
    """
    linhas = services.relatorio_pedidos_por_status()

    if not linhas:
        typer.echo("Nenhum pedido encontrado.")
        raise typer.Exit()

    typer.echo("Pedidos por status:")
    for linha in linhas:
        typer.echo(
            f"{linha['status']}: {linha['quantidade']} pedidos "
            f"({linha['percentual']:.2f}%)"
        )
