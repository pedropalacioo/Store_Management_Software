# loja/cli/cliente_cli.py
import typer
from typing import Optional

from loja import services

app = typer.Typer(help="Comandos relacionados a clientes.")


@app.command("cadastrar")
def cadastrar_cliente(
    nome: str = typer.Argument(..., help="Nome do cliente"),
    email: str = typer.Option(..., "--email", "-e", help="Email do cliente"),
    cpf: str = typer.Option(..., "--cpf", "-c", help="CPF do cliente"),
):
    """
    Cadastra um novo cliente.
    """
    cliente = services.cadastrar_cliente(nome=nome, email=email, cpf=cpf)
    typer.echo(f"✅ Cliente cadastrado com ID {cliente.id}.")


@app.command("listar")
def listar_clientes():
    """
    Lista todos os clientes.
    """
    clientes = services.listar_clientes()

    if not clientes:
        typer.echo("Nenhum cliente encontrado.")
        raise typer.Exit()

    for cli in clientes:
        typer.echo(f"[{cli.id}] {cli.nome} - {cli.email} - CPF: {cli.cpf}")


@app.command("detalhar")
def detalhar_cliente(
    cliente_id: int = typer.Argument(..., help="ID do cliente"),
):
    """
    Mostra detalhes de um cliente.
    """
    cliente = services.buscar_cliente_por_id(cliente_id)

    if not cliente:
        typer.echo("❌ Cliente não encontrado.")
        raise typer.Exit(code=1)

    typer.echo(f"ID: {cliente.id}")
    typer.echo(f"Nome: {cliente.nome}")
    typer.echo(f"Email: {cliente.email}")
    typer.echo(f"CPF: {cliente.cpf}")
    typer.echo(f"Endereços cadastrados: {len(cliente.endereco)}")


@app.command("adicionar-endereco")
def adicionar_endereco(
    cliente_id: int = typer.Argument(..., help="ID do cliente"),
    cep: str = typer.Option(..., "--cep"),
    cidade: str = typer.Option(..., "--cidade"),
    uf: str = typer.Option(..., "--uf"),
    logradouro: str = typer.Option(..., "--logradouro"),
    numero: str = typer.Option(..., "--numero"),
    complemento: Optional[str] = typer.Option(None, "--complemento"),
):
    """
    Adiciona um endereço ao cliente.
    """
    endereco = services.adicionar_endereco_cliente(
        cliente_id=cliente_id,
        cep=cep,
        cidade=cidade,
        uf=uf,
        logradouro=logradouro,
        numero=numero,
        complemento=complemento,
    )
    typer.echo(f"✅ Endereço {endereco.id} adicionado ao cliente {cliente_id}.")
