# loja/cli/pedido_cli.py
import typer
from typing import Optional

from loja import services

app = typer.Typer(help="Comandos relacionados a pedidos.")


@app.command("fechar")
def fechar_pedido(
    cliente_id: int = typer.Argument(..., help="ID do cliente"),
    endereco_id: int = typer.Option(..., "--endereco-id", "-e", help="Endereço de entrega"),
    cupom_codigo: Optional[str] = typer.Option(None, "--cupom", "-c", help="Código do cupom"),
):
    """
    Fecha um pedido a partir do carrinho do cliente.
    Calcula frete, aplica cupom, gera totais.
    """
    pedido = services.fechar_pedido(
        cliente_id=cliente_id,
        endereco_id=endereco_id,
        cupom_codigo=cupom_codigo,
    )

    typer.echo(f"✅ Pedido criado com ID {pedido.id}.")
    typer.echo(f"Status: {pedido.status}")
    typer.echo(f"Subtotal: R${pedido.subtotal:.2f}")
    typer.echo(f"Descontos: R${pedido.desconto:.2f}")
    typer.echo(f"Frete: R${pedido.valor_frete:.2f}")
    typer.echo(f"Total: R${pedido.total:.2f}")


@app.command("detalhar")
def detalhar_pedido(
    pedido_id: int = typer.Argument(..., help="ID do pedido"),
):
    """
    Mostra detalhes de um pedido.
    """
    pedido = services.buscar_pedido_por_id(pedido_id)

    if not pedido:
        typer.echo("❌ Pedido não encontrado.")
        raise typer.Exit(code=1)

    typer.echo(f"Pedido ID: {pedido.id} | Status: {pedido.status}")
    typer.echo(f"Cliente: {pedido.cliente.nome}")
    typer.echo("Itens:")
    for item in pedido.itens:
        typer.echo(
            f"- {item.produto.nome} (SKU {item.produto.sku}) "
            f"x {item.quantidade} = R${item.subtotal:.2f}"
        )
    typer.echo(f"Subtotal: R${pedido.subtotal:.2f}")
    typer.echo(f"Desconto: R${pedido.desconto:.2f}")
    typer.echo(f"Frete: R${pedido.valor_frete:.2f}")
    typer.echo(f"Total: R${pedido.total:.2f}")
    typer.echo(f"Endereço entrega: {pedido.endereco_entrega}")
    typer.echo(f"Criado em: {pedido.criado_em}")
    typer.echo(f"Pago em: {pedido.pago_em}")
    typer.echo(f"Enviado em: {pedido.enviado_em}")
    typer.echo(f"Entregue em: {pedido.entregue_em}")
    typer.echo(f"Cancelado em: {pedido.cancelado_em}")


@app.command("pagar")
def pagar_pedido(
    pedido_id: int = typer.Argument(..., help="ID do pedido"),
    valor: float = typer.Option(..., "--valor", "-v", help="Valor do pagamento"),
    forma: str = typer.Option(
        "PIX",
        "--forma",
        "-f",
        help="Forma de pagamento (PIX, CREDITO, DEBITO, BOLETO)",
    ),
):
    """
    Registra um pagamento (parcial ou total) para o pedido.
    """
    pagamento, pedido_atualizado = services.registrar_pagamento(
        pedido_id=pedido_id,
        valor=valor,
        forma=forma,
    )

    typer.echo(
        f"✅ Pagamento registrado (ID {pagamento.id}) no valor de R${pagamento.valor:.2f}."
    )
    typer.echo(f"Status atual do pedido: {pedido_atualizado.status}")


@app.command("enviar")
def enviar_pedido(
    pedido_id: int = typer.Argument(..., help="ID do pedido"),
):
    """
    Atualiza o pedido para ENVIADO e gera código de rastreio fictício.
    """
    pedido = services.enviar_pedido(pedido_id)
    typer.echo(f"✅ Pedido {pedido.id} marcado como ENVIADO.")
    typer.echo(f"Código de rastreio: {pedido.codigo_rastreio}")


@app.command("entregar")
def entregar_pedido(
    pedido_id: int = typer.Argument(..., help="ID do pedido"),
):
    """
    Marca o pedido como ENTREGUE.
    """
    pedido = services.marcar_pedido_entregue(pedido_id)
    typer.echo(f"✅ Pedido {pedido.id} marcado como ENTREGUE em {pedido.entregue_em}.")


@app.command("cancelar")
def cancelar_pedido(
    pedido_id: int = typer.Argument(..., help="ID do pedido"),
    motivo: Optional[str] = typer.Option(None, "--motivo", "-m", help="Motivo do cancelamento"),
):
    """
    Cancela um pedido (CRlADO ou PAGO) e faz estorno de estoque/valores conforme regras.
    """
    pedido = services.cancelar_pedido(pedido_id=pedido_id, motivo=motivo)
    typer.echo(f"✅ Pedido {pedido.id} cancelado com sucesso.")
    typer.echo(f"Status atual: {pedido.status}")
