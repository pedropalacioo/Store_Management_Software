import pytest

from src.cliente import Cliente
from src.endereco import Endereco


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def criar_endereco_valido(
    id_: int = 1,
    cep: str = "63000000",
    cidade: str = "Juazeiro do Norte",
    uf: str = "CE",
    logradouro: str = "Rua Teste",
    numero: str = "123",
    complemento: str | None = None,
) -> Endereco:
    """Cria um endereço válido para uso nos testes."""
    # o id_ é ignorado porque a classe Endereco gera o próprio id internamente
    return Endereco(cep, cidade, uf, logradouro, numero, complemento)


# ---------------------------------------------------------------------------
# Testes de criação de Cliente
# ---------------------------------------------------------------------------

def test_criacao_cliente_sem_enderecos_inicia_lista_vazia():
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901")

    assert cliente.nome == "Pedro"
    assert cliente.email == "pedro@example.com"
    assert cliente.cpf == "12345678901"
    assert isinstance(cliente.enderecos, list)
    assert len(cliente.enderecos) == 0


def test_criacao_cliente_com_enderecos_validos():
    end1 = criar_endereco_valido(1, "63000000")
    end2 = criar_endereco_valido(2, "63100000")

    cliente = Cliente("Kazuya", "kazuya@example.com", "10987654321", [end1, end2])

    assert len(cliente.enderecos) == 2
    assert cliente.enderecos[0] is end1
    assert cliente.enderecos[1] is end2


def test_criacao_cliente_enderecos_nao_lista_dispara_type_error():
    end = criar_endereco_valido()

    with pytest.raises(TypeError):
        Cliente("Pedro", "pedro@example.com", "12345678901", end)


def test_criacao_cliente_enderecos_com_item_nao_endereco_dispara_type_error():
    with pytest.raises(TypeError):
        Cliente("Pedro", "pedro@example.com", "12345678901", ["Rua A, 10"])


# ---------------------------------------------------------------------------
# Testes do setter de enderecos
# ---------------------------------------------------------------------------

def test_setter_enderecos_com_lista_valida():
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901")
    end1 = criar_endereco_valido()

    cliente.enderecos = [end1]

    assert len(cliente.enderecos) == 1
    assert cliente.enderecos[0] is end1


def test_setter_enderecos_com_item_invalido_dispara_type_error():
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901")

    with pytest.raises(TypeError):
        cliente.enderecos = ["Rua A, 10"]


# ---------------------------------------------------------------------------
# Testes de adicionar_endereco
# ---------------------------------------------------------------------------

def test_adicionar_endereco_valido():
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901")
    end = criar_endereco_valido()

    cliente.adicionar_endereco(end)

    assert len(cliente.enderecos) == 1
    assert cliente.enderecos[0] is end


def test_adicionar_endereco_tipo_invalido_dispara_type_error():
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901")

    with pytest.raises(TypeError):
        cliente.adicionar_endereco("Rua A, 10")  # não é Endereco


# ---------------------------------------------------------------------------
# Testes de remover_endereco / remover_endereco_indice
# ---------------------------------------------------------------------------

def test_remover_endereco_indice_valido():
    end1 = criar_endereco_valido(1)
    end2 = criar_endereco_valido(2)
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901", [end1, end2])

    cliente.remover_endereco_indice(0)

    assert len(cliente.enderecos) == 1
    assert cliente.enderecos[0] is end2


def test_remover_endereco_indice_tipo_invalido_dispara_type_error():
    end1 = criar_endereco_valido(1)
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901", [end1])

    with pytest.raises(TypeError):
        cliente.remover_endereco_indice("0")  # não é int


def test_remover_endereco_indice_fora_intervalo_dispara_value_error():
    end1 = criar_endereco_valido(1)
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901", [end1])

    with pytest.raises(ValueError):
        cliente.remover_endereco_indice(5)  # índice inválido


# ---------------------------------------------------------------------------
# Testes de validação de nome, email e cpf
# ---------------------------------------------------------------------------

def test_nome_vazio_dispara_value_error():
    with pytest.raises(ValueError):
        Cliente("", "pedro@example.com", "12345678901")


def test_email_invalido_dispara_value_error():
    with pytest.raises(ValueError):
        Cliente("Pedro", "email_invalido", "12345678901")


def test_cpf_invalido_dispara_value_error():
    with pytest.raises(ValueError):
        Cliente("Pedro", "pedro@example.com", "abc123")


# ---------------------------------------------------------------------------
# Testes de métodos especiais: __eq__, __repr__, __str__
# ---------------------------------------------------------------------------

def test_eq_retorna_true_quando_cpf_igual():
    end = criar_endereco_valido()
    c1 = Cliente("Pedro", "pedro1@example.com", "12345678901", [end])
    c2 = Cliente("Pedro", "pedro2@example.com", "12345678901", [end])

    assert c1 == c2


def test_eq_retorna_true_quando_email_igual():
    end = criar_endereco_valido()
    c1 = Cliente("Pedro", "pedro@example.com", "12345678901", [end])
    c2 = Cliente("Pedro", "pedro@example.com", "99999999999", [end])

    assert c1 == c2


def test_eq_retorna_false_quando_email_e_cpf_diferentes():
    c1 = Cliente("Pedro", "pedro1@example.com", "12345678901")
    c2 = Cliente("Ana", "ana@example.com", "99999999999")

    assert c1 != c2


def test_repr_retorna_string_com_informacoes_basicas():
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901")

    resultado = repr(cliente)

    assert isinstance(resultado, str)
    assert "Cliente(" in resultado
    assert "nome='" in resultado
    assert "email='" in resultado
    assert "cpf='" in resultado
    assert "enderecos=" in resultado


def test_str_retorna_string_mais_legivel():
    cliente = Cliente("Pedro", "pedro@example.com", "12345678901")

    resultado = str(cliente)

    assert isinstance(resultado, str)
    # aqui casamos com o formato do __str__ atual:
    assert "Cliente ID:" in resultado
    assert "Nome: Pedro" in resultado
    assert "Email: pedro@example.com" in resultado
    assert "CPF: 12345678901" in resultado
