"""
Simulação completa do fluxo de compra:
1. Criar cliente
2. Criar produto
3. Adicionar produto ao carrinho
4. Criar pedido
5. Aplicar cupom
6. Calcular frete
7. Registrar pagamento
"""

from datetime import datetime, date
from core.cliente import Cliente
from core.endereco import Endereco
from core.produto_fisico import ProdutoFisico
from core.item_carrinho import ItemCarrinho
from core.item_pedido import ItemPedido
from core.carrinho import Carrinho
from core.pedido import Pedido
from core.cupom import Cupom
from core.frete import Frete
from core.pagamento import Pagamento


def simular_fluxo_compra():
    """Simula um fluxo completo de compra na loja virtual"""
    
    print("=" * 70)
    print("SIMULAÇÃO DE FLUXO DE COMPRA - LOJA VIRTUAL")
    print("=" * 70)
    
    # ========== ETAPA 1: CRIAR CLIENTE ==========
    print("\n[1] CRIANDO CLIENTE...")
    print("-" * 70)
    
    endereco = Endereco(
        cep="01310100",
        cidade="São Paulo",
        numero="1000",
        UF="SP"
    )
    
    cliente = Cliente(
        nome="João Silva",
        email="joao.silva@email.com",
        cpf="12345678901",
        endereco=[endereco]
    )
    
    print(f"✓ Cliente criado com sucesso!")
    print(f"  Nome: {cliente.nome}")
    print(f"  Email: {cliente.email}")
    print(f"  CPF: {cliente.cpf}")
    print(f"  Endereço: Número {endereco.numero} - {endereco.cidade}/{endereco.UF}")
    print(f"  CEP: {endereco.cep}")
    
    # ========== ETAPA 2: CRIAR PRODUTO ==========
    print("\n[2] CRIANDO PRODUTO FÍSICO...")
    print("-" * 70)
    
    produto = ProdutoFisico(
        nome="Notebook Dell XPS 13",
        descricao="Notebook ultraportátil com processador Intel i7",
        preco=4500.00,
        peso=1.5,
        altura=18.0,
        largura=302.0,
        profundidade=199.0,
        sku="NB-DELL-XPS-13"
    )
    
    print(f"✓ Produto criado com sucesso!")
    print(f"  Nome: {produto.nome}")
    print(f"  SKU: {produto.sku}")
    print(f"  Preço: R$ {produto.preco:.2f}")
    print(f"  Peso: {produto.peso} kg")
    print(f"  Dimensões: {produto.altura}x{produto.largura}x{produto.profundidade} mm")
    
    # ========== ETAPA 3: CRIAR CARRINHO E ADICIONAR ITEM ==========
    print("\n[3] CRIANDO CARRINHO E ADICIONANDO PRODUTO...")
    print("-" * 70)
    
    item_carrinho = ItemCarrinho(
        produto=produto,
        quantidade=1,
        preco_unitario=produto.preco
    )
    
    carrinho = Carrinho(
        cliente=cliente,
        itens=[item_carrinho],
        criado_em=datetime.now(),
        atualizado_em=datetime.now(),
        ativo=True
    )
    
    print(f"✓ Carrinho criado com sucesso!")
    print(f"  Cliente: {carrinho.cliente.nome}")
    print(f"  Quantidade de itens: {len(carrinho.itens)}")
    
    subtotal_carrinho = sum(item.quantidade * item.preco_unitario for item in carrinho.itens)
    print(f"  Subtotal do carrinho: R$ {subtotal_carrinho:.2f}")
    print(f"\n  Item no carrinho:")
    print(f"    - {item_carrinho.produto.nome}")
    print(f"      Quantidade: {item_carrinho.quantidade}")
    print(f"      Preço unitário: R$ {item_carrinho.preco_unitario:.2f}")
    print(f"      Subtotal: R$ {item_carrinho.quantidade * item_carrinho.preco_unitario:.2f}")
    
    # ========== ETAPA 4: CRIAR CUPOM ==========
    print("\n[4] CRIANDO CUPOM DE DESCONTO...")
    print("-" * 70)
    
    cupom = Cupom(
        codigo="DESCONTO10",
        tipo="PERCENTUAL",
        valor=10.0,
        data_validade=date(2025, 12, 31),
        uso_maximo=100,
        categorias_elegiveis=[]
    )
    
    print(f"✓ Cupom criado com sucesso!")
    print(f"  Código: {cupom.codigo}")
    print(f"  Tipo: {cupom.tipo}")
    print(f"  Valor de desconto: {cupom.valor}%")
    print(f"  Válido até: {cupom.data_validade}")
    
    # ========== ETAPA 5: CALCULAR DESCONTO ==========
    print("\n[5] APLICANDO DESCONTO COM CUPOM...")
    print("-" * 70)
    
    desconto = (subtotal_carrinho * cupom.valor) / 100
    subtotal_com_desconto = subtotal_carrinho - desconto
    
    print(f"✓ Cupom aplicável!")
    print(f"  Subtotal: R$ {subtotal_carrinho:.2f}")
    print(f"  Desconto ({cupom.valor}%): R$ {desconto:.2f}")
    print(f"  Subtotal com desconto: R$ {subtotal_com_desconto:.2f}")
    
    # ========== ETAPA 6: CALCULAR FRETE ==========
    print("\n[6] CALCULANDO FRETE...")
    print("-" * 70)
    
    frete = Frete.from_frete(endereco.UF)
    
    print(f"✓ Frete calculado com sucesso!")
    print(f"  Destino: {frete.uf}")
    print(f"  Valor do frete: R$ {frete.valor:.2f}")
    print(f"  Prazo de entrega: {frete.prazo_entrega} dias úteis")
    
    # ========== ETAPA 7: CRIAR PEDIDO ==========
    print("\n[7] CRIANDO PEDIDO A PARTIR DO CARRINHO...")
    print("-" * 70)
    
    item_pedido = ItemPedido(
        produto=produto,
        quantidade=item_carrinho.quantidade,
        preco_unitario=item_carrinho.preco_unitario
    )
    
    pedido = Pedido(
        cliente=cliente,
        endereco_entrega=endereco,
        itens=[item_pedido],
        cupom=cupom,
        frete=frete,
        criado_em=datetime.now()
    )
    
    total_pedido = subtotal_com_desconto + frete.valor
    
    print(f"✓ Pedido criado com sucesso!")
    print(f"  Número do pedido: PED-{id(pedido)}")
    print(f"  Cliente: {pedido.cliente.nome}")
    print(f"  Status: PENDENTE")
    print(f"  Data de criação: {pedido.criado_em.strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"  Quantidade de itens: {len(pedido.itens)}")
    print(f"  Subtotal: R$ {subtotal_carrinho:.2f}")
    print(f"  Desconto (cupom): R$ {desconto:.2f}")
    print(f"  Frete: R$ {frete.valor:.2f}")
    print(f"  Total do pedido: R$ {total_pedido:.2f}")
    
    # ========== ETAPA 8: REGISTRAR PAGAMENTO ==========
    print("\n[8] REGISTRANDO PAGAMENTO...")
    print("-" * 70)
    
    total_pedido = subtotal_com_desconto + frete.valor
    
    pagamento = Pagamento(
        pedido=pedido,
        data_pagamento=datetime.now(),
        forma="CREDITO",
        valor=total_pedido
    )
    
    print(f"✓ Pagamento registrado com sucesso!")
    print(f"  Pedido: PED-{id(pedido)}")
    print(f"  Valor: R$ {pagamento.valor:.2f}")
    print(f"  Forma: {pagamento.forma}")
    print(f"  Status: {'Confirmado' if pagamento.confirmado else 'Pendente'}")
    
    # ========== ETAPA 9: CONFIRMAR PAGAMENTO ==========
    print("\n[9] CONFIRMANDO PAGAMENTO...")
    print("-" * 70)
    
    if hasattr(pagamento, 'confirmar'):
        pagamento.confirmar()
    
    print(f"✓ Pagamento confirmado com sucesso!")
    print(f"  Status do pagamento: {'Confirmado' if pagamento.confirmado else 'Pendente'}")
    print(f"  Status do pedido: {pedido.status}")
    
    # ========== RESUMO FINAL ==========
    print("\n" + "=" * 70)
    print("RESUMO FINAL DO PEDIDO")
    print("=" * 70)
    
    print(f"\n📋 DADOS DO CLIENTE")
    print(f"  Nome: {cliente.nome}")
    print(f"  Email: {cliente.email}")
    print(f"  CPF: {cliente.cpf}")
    print(f"  Endereço: Rua nº {endereco.numero}, {endereco.cidade}/{endereco.UF}")
    
    print(f"\n📦 ITENS DO PEDIDO")
    print(f"  Produto: {item_carrinho.produto.nome}")
    print(f"  Quantidade: {item_carrinho.quantidade}")
    print(f"  Preço unitário: R$ {item_carrinho.preco_unitario:.2f}")
    print(f"  Subtotal: R$ {item_carrinho.quantidade * item_carrinho.preco_unitario:.2f}")
    
    print(f"\n💰 VALORES")
    print(f"  Subtotal: R$ {subtotal_carrinho:.2f}")
    print(f"  Cupom ({cupom.codigo}): -R$ {desconto:.2f}")
    print(f"  Frete: R$ {frete.valor:.2f}")
    print(f"  Total: R$ {total_pedido:.2f}")
    
    print(f"\n💳 PAGAMENTO")
    print(f"  Forma: {pagamento.forma}")
    print(f"  Status: {'Confirmado' if pagamento.confirmado else 'Pendente'}")
    
    return {
        "cliente": cliente,
        "produto": produto,
        "carrinho": carrinho,
        "cupom": cupom,
        "frete": frete,
        "pedido": pedido,
        "pagamento": pagamento
    }


if __name__ == "__main__":
    try:
        resultado = simular_fluxo_compra()
        
        print("\n" + "=" * 70)
        print("✅ SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 70)
        print(f"\n📊 Objetos criados:")
        print(f"  ✓ Cliente: {resultado['cliente'].nome}")
        print(f"  ✓ Produto: {resultado['produto'].nome}")
        print(f"  ✓ Carrinho: {len(resultado['carrinho'].itens)} item(ns)")
        print(f"  ✓ Cupom: {resultado['cupom'].codigo}")
        print(f"  ✓ Frete: R$ {resultado['frete'].valor:.2f}")
        print(f"  ✓ Pedido: Número PED-{id(resultado['pedido'])}")
        print(f"  ✓ Pagamento: {'Confirmado' if resultado['pagamento'].confirmado else 'Pendente'}")
        
    except Exception as e:
        print(f"\n❌ Erro durante a simulação: {e}")
        import traceback
        traceback.print_exc()