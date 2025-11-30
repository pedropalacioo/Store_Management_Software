import pytest

from src.carrinho import Carrinho
from src.produto import Produto
from src.item_carrinho import ItemCarrinho

# -------------------------
# FIXTURES
# -------------------------
@pytest.fixture
def produto1():
    return Produto(
        nome="Produto 1",
        categoria="Categoria A",
        preco=10.0,
        estoque=100,
        ativo=True
    )


@pytest.fixture
def produto2():
    return Produto(
        nome="Produto 2",
        categoria="Categoria B",
        preco=20.0,
        estoque=50,
        ativo=True
    )


@pytest.fixture
def carrinho_vazio():
    return Carrinho(cliente="Cliente Teste")


@pytest.fixture
def carrinho_com_itens(produto1, produto2):
    c = Carrinho(cliente="Cliente Teste")
    c.adicionar_item(produto1, quantidade=2)  # subtotal = 2 * 10 = 20
    c.adicionar_item(produto2, quantidade=1)  # subtotal = 1 * 20 = 20
    return c


# -------------------------
# TESTES BÁSICOS DE CRIAÇÃO
# -------------------------
def test_criacao_carrinho(carrinho_vazio):
    assert carrinho_vazio.cliente == "Cliente Teste"
    assert carrinho_vazio.itens == []
    assert carrinho_vazio.ativo is True
    assert carrinho_vazio.criado_em is None
    assert carrinho_vazio.atualizado_em is None
    assert isinstance(carrinho_vazio.id, int)


# -------------------------
# TESTES: adicionar_item
# -------------------------
def test_adicionar_item_novo_produto(carrinho_vazio, produto1):
    carrinho_vazio.adicionar_item(produto1, quantidade=3)
    assert len(carrinho_vazio.itens) == 1
    item = carrinho_vazio.itens[0]
    assert item.produto is produto1
    assert item.quantidade == 3
    assert item.preco_unitario == produto1.preco


def test_adicionar_item_soma_quantidade_se_mesmo_sku(carrinho_vazio, produto1):
    carrinho_vazio.adicionar_item(produto1, quantidade=1)
    carrinho_vazio.adicionar_item(produto1, quantidade=2)
    assert len(carrinho_vazio.itens) == 1
    item = carrinho_vazio.itens[0]
    assert item.quantidade == 3  # 1 + 2


def test_adicionar_item_quantidade_invalida(carrinho_vazio, produto1):
    with pytest.raises(ValueError):
        carrinho_vazio.adicionar_item(produto1, quantidade=0)


# -------------------------
# TESTES: remover_item
# -------------------------
def test_remover_item_existente(carrinho_com_itens, produto1):
    sku = produto1.sku
    carrinho_com_itens.remover_item(sku)
    # agora só deve restar 1 item
    assert len(carrinho_com_itens.itens) == 1
    assert all(item.produto.sku != sku for item in carrinho_com_itens.itens)


def test_remover_item_inexistente(carrinho_com_itens):
    with pytest.raises(ValueError):
        carrinho_com_itens.remover_item("SKU_INEXISTENTE")


# -------------------------
# TESTES: alterar_quantidade
# -------------------------
def test_alterar_quantidade_valida(carrinho_com_itens, produto1):
    sku = produto1.sku
    carrinho_com_itens.alterar_quantidade(sku, nova_quantidade=5)
    for item in carrinho_com_itens.itens:
        if item.produto.sku == sku:
            assert item.quantidade == 5
            break
    else:
        pytest.fail("Item com SKU não encontrado no carrinho.")


def test_alterar_quantidade_menor_que_um_dispara_erro(carrinho_com_itens, produto1):
    sku = produto1.sku
    with pytest.raises(ValueError):
        carrinho_com_itens.alterar_quantidade(sku, nova_quantidade=0)


def test_alterar_quantidade_item_inexistente(carrinho_com_itens):
    with pytest.raises(ValueError):
        carrinho_com_itens.alterar_quantidade("SKU_INEXISTENTE", nova_quantidade=3)


# -------------------------
# TESTES: calcular_subtotal
# -------------------------
def test_calcular_subtotal(carrinho_com_itens):
    # produto1: 2 * 10 = 20
    # produto2: 1 * 20 = 20
    # total = 40
    assert carrinho_com_itens.calcular_subtotal() == 40.0


# -------------------------
# TESTES: limpar
# -------------------------
def test_limpar_carrinho(carrinho_com_itens):
    carrinho_com_itens.limpar()
    assert carrinho_com_itens.itens == []


# -------------------------
# TESTES: ativo (getter/setter)
# -------------------------
def test_ativo_set_valido(carrinho_vazio):
    carrinho_vazio.ativo = False
    assert carrinho_vazio.ativo is False


def test_ativo_set_invalido(carrinho_vazio):
    with pytest.raises(TypeError):
        carrinho_vazio.ativo = "sim"


# -------------------------
# TESTES: criado_em / atualizado_em
# -------------------------
def test_criado_em_atualizado_em_devem_ser_none(carrinho_vazio):
    # setter aceita None
    carrinho_vazio.criado_em = None
    carrinho_vazio.atualizado_em = None
    assert carrinho_vazio.criado_em is None
    assert carrinho_vazio.atualizado_em is None


def test_criado_em_set_valor_nao_none_dispara_erro(carrinho_vazio):
    with pytest.raises(TypeError):
        carrinho_vazio.criado_em = "2025-11-30"


def test_atualizado_em_set_valor_nao_none_dispara_erro(carrinho_vazio):
    with pytest.raises(TypeError):
        carrinho_vazio.atualizado_em = "2025-11-30"


# -------------------------
# TESTES: __len__
# -------------------------
def test_len_retorna_quantidade_total_itens(carrinho_com_itens, produto1):
    """
    Esperado pelo enunciado: __len__ deve representar a quantidade
    total de itens no carrinho (somando as quantidades).
    """
    # No fixture: produto1 (2 unidades) + produto2 (1 unidade) = 3
    # O teste espera que você implemente __len__ retornando um int,
    # não uma string.
    assert len(carrinho_com_itens) == 3


# -------------------------
# TESTES: __str__ e __repr__
# -------------------------
def test_str_carrinho(carrinho_vazio):
    texto = str(carrinho_vazio)
    assert "Carrinho ID [" in texto
    assert "Cliente:" in texto


def test_repr_carrinho(carrinho_vazio):
    texto = repr(carrinho_vazio)
    assert "Carrinho (id:" in texto
    assert "cliente:" in texto