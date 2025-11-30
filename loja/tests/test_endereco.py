import pytest

from src.endereco import Endereco

# ------------------------------
# FIXTURE DE UM OBJETO VÁLIDO
# ------------------------------
@pytest.fixture
def endereco_valido():
    return Endereco(
        cep="63000000",
        cidade="Juazeiro do Norte",
        uf="CE",
        logradouro="Rua A",
        numero="123",
        complemento="Casa"
    )

# ------------------------------
# TESTE: CRIAÇÃO DO OBJETO
# ------------------------------
def test_criacao_endereco(endereco_valido):
    assert endereco_valido.cep == "63000000"
    assert endereco_valido.cidade == "Juazeiro do Norte"
    assert endereco_valido.uf == "CE"
    assert endereco_valido.logradouro == "Rua A"
    assert endereco_valido.numero == "123"
    assert endereco_valido.complemento == "Casa"

# ------------------------------
# TESTE: ID É GERADO AUTOMATICAMENTE
# ------------------------------
def test_id_gerado_automaticamente(endereco_valido):
    assert isinstance(endereco_valido.id, int)
    assert 0 <= endereco_valido.id <= 9999

# ------------------------------
# TESTE: CEP VÁLIDO
# ------------------------------
def test_atualizar_cep_valido(endereco_valido):
    endereco_valido.cep = "12345678"
    assert endereco_valido.cep == "12345678"

# ------------------------------
# TESTE: CEP INVÁLIDO (NÃO STRING)
# ------------------------------
def test_cep_invalido_tipo():
    with pytest.raises(TypeError):
        Endereco("12345678", "Cidade", "CE", "Rua", "10", None).cep = 12345678

# ------------------------------
# TESTE: CEP INVÁLIDO (TAMANHO DIFERENTE DE 8)
# ------------------------------
def test_cep_invalido_tamanho(endereco_valido):
    with pytest.raises(ValueError):
        endereco_valido.cep = "123"

# ------------------------------
# TESTE: CEP INVÁLIDO (NÃO NUMÉRICO)
# ------------------------------
def test_cep_invalido_nao_numerico(endereco_valido):
    with pytest.raises(ValueError):
        endereco_valido.cep = "ABCDEF12"

# ------------------------------
# TESTE: UF VÁLIDO
# ------------------------------
def test_uf_valida(endereco_valido):
    endereco_valido.uf = "sp"
    assert endereco_valido.uf == "SP"  # deve converter para maiúsculo

# ------------------------------
# TESTE: UF INVÁLIDA (TAMANHO != 2)
# ------------------------------
def test_uf_invalida(endereco_valido):
    with pytest.raises(ValueError):
        endereco_valido.uf = "CES"

# ------------------------------
# TESTE: LOGRADOURO INVÁLIDO
# ------------------------------
def test_logradouro_invalido(endereco_valido):
    with pytest.raises(TypeError):
        endereco_valido.logradouro = 1234

# ------------------------------
# TESTE: NÚMERO INVÁLIDO
# ------------------------------
def test_numero_invalido(endereco_valido):
    with pytest.raises(TypeError):
        endereco_valido.numero = 10

# ------------------------------
# TESTE: COMPLEMENTO INVÁLIDO
# ------------------------------
def test_complemento_invalido(endereco_valido):
    with pytest.raises(TypeError):
        endereco_valido.complemento = 999

# ------------------------------
# TESTE: COMPLEMENTO NONE
# ------------------------------
def test_complemento_none(endereco_valido):
    endereco_valido.complemento = None
    assert endereco_valido.complemento is None

# ------------------------------
# TESTE: MÉTODO formatar()
# ------------------------------
def test_formatar(endereco_valido):
    texto = endereco_valido.formatar()
    assert "CEP:" in texto
    assert "Juazeiro do Norte" in texto
    assert "Rua A" in texto

# ------------------------------
# TESTE: __str__ RETORNA formatar()
# ------------------------------
def test_str(endereco_valido):
    assert str(endereco_valido) == endereco_valido.formatar()