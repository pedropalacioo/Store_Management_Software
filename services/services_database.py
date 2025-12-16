"""
Serviços de Validação no Banco de Dados.
Valida regras de negócio que dependem do estado do banco.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("db/database.db")

# Constantes
LIMITE_MAXIMO_ITENS_CARRINHO = 50


class ValidacaoDatabaseError(Exception):
    """Exceção para erros de validação no banco de dados"""
    pass


# ============================================================================
# VALIDAÇÕES DE PRODUTO
# ============================================================================

def validar_sku_unico(sku: str, produto_id: int = None) -> bool:
    """
    Valida se o SKU é único no banco (não há outro produto com mesmo SKU).
    
    Args:
        sku: SKU a validar
        produto_id: ID do produto (para exclusão ao atualizar)
    
    Returns:
        True se SKU é único, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se SKU é vazio ou None
    """
    if not sku or not isinstance(sku, str):
        raise ValidacaoDatabaseError("SKU não pode ser vazio")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            if produto_id:
                # Se atualizando, exclui o produto atual da busca
                cursor.execute(
                    "SELECT COUNT(*) FROM produtos WHERE sku = ? AND id != ?;",
                    (sku, produto_id)
                )
            else:
                # Se criando, busca qualquer produto com esse SKU
                cursor.execute(
                    "SELECT COUNT(*) FROM produtos WHERE sku = ?;",
                    (sku,)
                )
            
            count = cursor.fetchone()[0]
            return count == 0
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar SKU: {str(e)}")


# ============================================================================
# VALIDAÇÕES DE CLIENTE
# ============================================================================

def validar_cpf_unico(cpf: str, cliente_id: int = None) -> bool:
    """
    Valida se o CPF é único no banco.
    
    Args:
        cpf: CPF a validar
        cliente_id: ID do cliente (para exclusão ao atualizar)
    
    Returns:
        True se CPF é único, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se CPF é inválido
    """
    if not cpf or not isinstance(cpf, str):
        raise ValidacaoDatabaseError("CPF não pode ser vazio")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            if cliente_id:
                cursor.execute(
                    "SELECT COUNT(*) FROM clientes WHERE cpf = ? AND id != ?;",
                    (cpf, cliente_id)
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM clientes WHERE cpf = ?;",
                    (cpf,)
                )
            
            count = cursor.fetchone()[0]
            return count == 0
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar CPF: {str(e)}")


def validar_email_unico(email: str, cliente_id: int = None) -> bool:
    """
    Valida se o email é único no banco.
    
    Args:
        email: Email a validar
        cliente_id: ID do cliente (para exclusão ao atualizar)
    
    Returns:
        True se email é único, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se email é inválido
    """
    if not email or not isinstance(email, str):
        raise ValidacaoDatabaseError("Email não pode ser vazio")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            if cliente_id:
                cursor.execute(
                    "SELECT COUNT(*) FROM clientes WHERE email = ? AND id != ?;",
                    (email, cliente_id)
                )
            else:
                cursor.execute(
                    "SELECT COUNT(*) FROM clientes WHERE email = ?;",
                    (email,)
                )
            
            count = cursor.fetchone()[0]
            return count == 0
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar email: {str(e)}")


def validar_cliente_existe(cpf: str) -> bool:
    """
    Valida se um cliente existe no banco pelo CPF.
    
    Args:
        cpf: CPF do cliente
    
    Returns:
        True se cliente existe, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se CPF é inválido
    """
    if not cpf or not isinstance(cpf, str):
        raise ValidacaoDatabaseError("CPF não pode ser vazio")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM clientes WHERE cpf = ?;", (cpf,))
            count = cursor.fetchone()[0]
            return count > 0
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar existência do cliente: {str(e)}")


def obter_cliente_id(cpf: str) -> int | None:
    """
    Obtém o ID de um cliente pelo CPF.
    
    Args:
        cpf: CPF do cliente
    
    Returns:
        ID do cliente ou None se não encontrado
    
    Raises:
        ValidacaoDatabaseError: Se CPF é inválido
    """
    if not cpf or not isinstance(cpf, str):
        raise ValidacaoDatabaseError("CPF não pode ser vazio")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM clientes WHERE cpf = ?;", (cpf,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao obter ID do cliente: {str(e)}")


# ============================================================================
# VALIDAÇÕES DE CUPOM
# ============================================================================

def validar_cupom_existe(codigo: str) -> bool:
    """
    Valida se um cupom existe no banco.
    
    Args:
        codigo: Código do cupom
    
    Returns:
        True se cupom existe, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se código é inválido
    """
    if not codigo or not isinstance(codigo, str):
        raise ValidacaoDatabaseError("Código do cupom não pode ser vazio")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cupons WHERE codigo = ?;", (codigo,))
            count = cursor.fetchone()[0]
            return count > 0
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar cupom: {str(e)}")


def validar_cupom_ativo(codigo: str) -> bool:
    """
    Valida se um cupom está ativo no banco.
    
    Args:
        codigo: Código do cupom
    
    Returns:
        True se cupom está ativo, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se cupom não existe
    """
    if not codigo or not isinstance(codigo, str):
        raise ValidacaoDatabaseError("Código do cupom não pode ser vazio")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ativo FROM cupons WHERE codigo = ?;", (codigo,))
            resultado = cursor.fetchone()
            
            if not resultado:
                raise ValidacaoDatabaseError(f"Cupom '{codigo}' não encontrado")
            
            return bool(resultado[0])
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar cupom ativo: {str(e)}")


def validar_cupom_valor_minimo(codigo: str, valor_compra: float) -> bool:
    """
    Valida se o valor de compra atende ao mínimo do cupom.
    
    Args:
        codigo: Código do cupom
        valor_compra: Valor da compra
    
    Returns:
        True se valor atende ao mínimo, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se cupom não existe
    """
    if not codigo or not isinstance(codigo, str):
        raise ValidacaoDatabaseError("Código do cupom não pode ser vazio")
    
    if valor_compra < 0:
        raise ValidacaoDatabaseError("Valor de compra não pode ser negativo")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT valor_minimo_compra FROM cupons WHERE codigo = ?;",
                (codigo,)
            )
            resultado = cursor.fetchone()
            
            if not resultado:
                raise ValidacaoDatabaseError(f"Cupom '{codigo}' não encontrado")
            
            valor_minimo = resultado[0]
            return valor_compra >= valor_minimo
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar valor mínimo do cupom: {str(e)}")


# ============================================================================
# VALIDAÇÕES DE CARRINHO
# ============================================================================

def validar_limite_itens_carrinho(quantidade_atual: int, novo_item_quantidade: int = 1) -> bool:
    """
    Valida se a adição de um novo item não excede o limite máximo.
    
    Args:
        quantidade_atual: Quantidade atual de itens no carrinho
        novo_item_quantidade: Quantidade de itens a adicionar
    
    Returns:
        True se está dentro do limite, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se quantidades são inválidas
    """
    if quantidade_atual < 0 or novo_item_quantidade < 1:
        raise ValidacaoDatabaseError("Quantidades inválidas")
    
    total = quantidade_atual + novo_item_quantidade
    
    if total > LIMITE_MAXIMO_ITENS_CARRINHO:
        raise ValidacaoDatabaseError(
            f"Limite de {LIMITE_MAXIMO_ITENS_CARRINHO} itens no carrinho excedido. "
            f"Atual: {quantidade_atual}, tentando adicionar: {novo_item_quantidade}"
        )
    
    return True


# ============================================================================
# VALIDAÇÕES DE PEDIDO
# ============================================================================

def validar_pedido_cliente_existe(cpf_cliente: str) -> bool:
    """
    Valida se cliente do pedido existe.
    
    Args:
        cpf_cliente: CPF do cliente
    
    Returns:
        True se cliente existe, False caso contrário
    """
    return validar_cliente_existe(cpf_cliente)


def validar_pedido_endereco_valido(cep: str, numero, cidade: str, uf: str) -> bool:
    """
    Valida se endereço do pedido é válido.
    
    Args:
        cep: CEP do endereço (8 dígitos)
        numero: Número do endereço (int ou str)
        cidade: Cidade do endereço
        uf: UF do endereço (2 caracteres)
    
    Returns:
        True se endereço é válido, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se dados do endereço são inválidos
    """
    # Validação de CEP
    if not cep or not isinstance(cep, str):
        raise ValidacaoDatabaseError("CEP inválido: deve ser string")
    
    if len(cep) != 8:
        raise ValidacaoDatabaseError(f"CEP inválido: deve ter exatamente 8 caracteres, recebido {len(cep)}")
    
    if not cep.isdigit():
        raise ValidacaoDatabaseError("CEP inválido: deve conter apenas dígitos")
    
    # Validação de número
    try:
        num_value = int(numero) if isinstance(numero, str) else numero
        if num_value < 1:
            raise ValidacaoDatabaseError("Número deve ser maior que 0")
    except (ValueError, TypeError):
        raise ValidacaoDatabaseError("Número inválido: deve ser numérico")
    
    # Validação de cidade
    if not cidade or not isinstance(cidade, str):
        raise ValidacaoDatabaseError("Cidade inválida")
    
    # Validação de UF
    if not uf or len(uf) != 2:
        raise ValidacaoDatabaseError("UF deve ter exatamente 2 caracteres")
    
    # UFs válidas do Brasil
    ufs_validas = {'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
                   'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
                   'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'}
    
    if uf.upper() not in ufs_validas:
        raise ValidacaoDatabaseError(f"UF '{uf}' não é válida")
    
    return True


def validar_pedido_cupom_valido(codigo_cupom: str, valor_pedido: float) -> bool:
    """
    Valida se cupom é válido para o pedido.
    
    Args:
        codigo_cupom: Código do cupom
        valor_pedido: Valor do pedido (subtotal)
    
    Returns:
        True se cupom é válido, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se cupom é inválido
    """
    # Validar que cupom existe
    if not validar_cupom_existe(codigo_cupom):
        raise ValidacaoDatabaseError(f"Cupom '{codigo_cupom}' não encontrado")
    
    # Validar que cupom está ativo
    if not validar_cupom_ativo(codigo_cupom):
        raise ValidacaoDatabaseError(f"Cupom '{codigo_cupom}' não está ativo")
    
    # Validar que valor atende ao mínimo
    if not validar_cupom_valor_minimo(codigo_cupom, valor_pedido):
        raise ValidacaoDatabaseError(
            f"Valor do pedido não atende ao mínimo exigido pelo cupom '{codigo_cupom}'"
        )
    
    return True


# ============================================================================
# VALIDAÇÕES DE ESTOQUE
# ============================================================================

def validar_estoque_suficiente(sku: str, quantidade: int) -> bool:
    """
    Valida se há estoque suficiente de um produto.
    
    Args:
        sku: SKU do produto
        quantidade: Quantidade desejada
    
    Returns:
        True se há estoque, False caso contrário
    
    Raises:
        ValidacaoDatabaseError: Se produto não existe ou quantidade é inválida
    """
    if not sku or not isinstance(sku, str):
        raise ValidacaoDatabaseError("SKU inválido")
    
    if quantidade < 1:
        raise ValidacaoDatabaseError("Quantidade deve ser maior que 0")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT estoque FROM produtos WHERE sku = ?;",
                (sku,)
            )
            resultado = cursor.fetchone()
            
            if not resultado:
                raise ValidacaoDatabaseError(f"Produto com SKU '{sku}' não encontrado")
            
            estoque = resultado[0]
            return estoque >= quantidade
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao validar estoque: {str(e)}")


def obter_estoque_produto(sku: str) -> int:
    """
    Obtém a quantidade em estoque de um produto.
    
    Args:
        sku: SKU do produto
    
    Returns:
        Quantidade em estoque
    
    Raises:
        ValidacaoDatabaseError: Se produto não existe
    """
    if not sku or not isinstance(sku, str):
        raise ValidacaoDatabaseError("SKU inválido")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT estoque FROM produtos WHERE sku = ?;",
                (sku,)
            )
            resultado = cursor.fetchone()
            
            if not resultado:
                raise ValidacaoDatabaseError(f"Produto com SKU '{sku}' não encontrado")
            
            return resultado[0]
    except sqlite3.Error as e:
        raise ValidacaoDatabaseError(f"Erro ao obter estoque: {str(e)}")
