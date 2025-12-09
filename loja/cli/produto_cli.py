# loja/cli/produto_cli.py
import typer
from typing import Optional

from loja.services import services  # ajuste se seu services estiver em outro lugar

app = typer.Typer(help="Comandos relacionados a produtos.")


@app.command("cadastrar")
def cadastrar_produto(
    nome: str = typer.Argument(..., help="Nome do produto"),
    categoria: str = typer.Option("geral", "--categoria", "-c", help="Categoria do produto"),
    preco: float = typer.Option(..., "--preco", "-p", help="Preço unitário (>0)"),
    estoque: int = typer.Option(0, "--estoque", "-e", help="Quantidade em estoque (>=0)"),
):
    """
    Cadastra um novo produto.
    """
    produto = services.cadastrar_produto(
        nome=nome,
        categoria=categoria,
        preco=preco,
        estoque=estoque,
    )
    typer.echo(f"✅ Produto cadastrado com SKU {produto.sku}.")


@app.command("listar")
def listar_produtos(
    apenas_ativos: bool = typer.Option(
        False, "--ativos", help="Listar apenas produtos ativos."
    )
):
    """
    Lista produtos cadastrados.
    """
    produtos = services.listar_produtos(ativos=apenas_ativos)

    if not produtos:
        typer.echo("Nenhum produto encontrado.")
        raise typer.Exit()

    for p in produtos:
        status = "ativo" if p.ativo else "inativo"
        typer.echo(f"[{p.sku}] {p.nome} - R${p.preco:.2f} - estoque: {p.estoque} ({status})")


@app.command("detalhar")
def detalhar_produto(
    sku: int = typer.Argument(..., help="SKU do produto"),
):
    """
    Mostra detalhes de um produto.
    """
    produto = services.buscar_produto_por_sku(sku)

    if not produto:
        typer.echo("❌ Produto não encontrado.")
        raise typer.Exit(code=1)

    typer.echo(f"SKU: {produto.sku}")
    typer.echo(f"Nome: {produto.nome}")
    typer.echo(f"Categoria: {produto.categoria}")
    typer.echo(f"Preço: R${produto.preco:.2f}")
    typer.echo(f"Estoque: {produto.estoque}")
    typer.echo(f"Ativo: {produto.ativo}")


@app.command("atualizar")
def atualizar_produto(
    sku: int = typer.Argument(..., help="SKU do produto"),
    nome: Optional[str] = typer.Option(None, "--nome", help="Novo nome"),
    categoria: Optional[str] = typer.Option(None, "--categoria", help="Nova categoria"),
    preco: Optional[float] = typer.Option(None, "--preco", help="Novo preço"),
    ativo: Optional[bool] = typer.Option(None, "--ativo/--inativo", help="Alterar status"),
):
    """
    Atualiza campos de um produto.
    """
    produto = services.atualizar_produto(
        sku=sku,
        nome=nome,
        categoria=categoria,
        preco=preco,
        ativo=ativo,
    )

    typer.echo(f"✅ Produto {produto.sku} atualizado com sucesso.")


@app.command("ajustar-estoque")
def ajustar_estoque(
    sku: int = typer.Argument(..., help="SKU do produto"),
    quantidade: int = typer.Argument(..., help="Quantidade (pode ser negativa)"),
):
    """
    Ajusta o estoque de um produto (entrada ou saída).
    """
    produto = services.ajustar_estoque_produto(sku=sku, quantidade=quantidade)
    typer.echo(
        f"✅ Estoque do produto {produto.sku} ajustado. Novo estoque: {produto.estoque}"
    )
