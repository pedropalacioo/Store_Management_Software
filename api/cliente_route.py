from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr

import db.database as database
from core.cliente import Cliente
from core.endereco import Endereco

router = APIRouter(
    prefix = "/clientes",
    tags = ["Clientes"],
)

# Modelos Pydantic

class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    cpf: str

class ClienteUpdateNome(BaseModel):
    nome: str

class ClienteUpdateEmail(BaseModel):
    email: EmailStr

class EnderecoCreate(BaseModel):
    cep: str
    numero: str
    cidade: str
    UF: str

class EnderecoUpdate(BaseModel):
    cep: str | None = None
    numero: str | None = None
    cidade: str | None = None
    UF: str | None = None

class EnderecoResponse(BaseModel):
    cep: str
    numero: str
    cidade: str
    UF: str

class clienteResponse(BaseModel):
    nome: str
    email: EmailStr
    cpf: str

class ClienteComEnderecosResponse(BaseModel):
    nome: str
    email: str
    cpf: str
    enderecos: list[EnderecoResponse]

# Rotas CREATE
@router.post("/", response_model = clienteResponse, status_code = status.HTTP_201_CREATED)
def criar_cliente(cliente: ClienteCreate):
    novo_cliente = Cliente(
        nome = cliente.nome,
        email = cliente.email,
        cpf = cliente.cpf,
    )
    database.salvar_cliente(novo_cliente)
    return novo_cliente

# Rotas READ
@router.get("/")
def listar_clientes() -> list[clienteResponse]:
    clientes = database.carregar_clientes()
    return clientes

@router.get("/{cpf}")
def buscar_cliente(cpf: str) -> clienteResponse:
    clientes = database.carregar_clientes()
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")

# Rotas UPDATE
# NOME
@router.patch("/{cpf}/nome", response_model = clienteResponse)
def atualizar_cliente_nome(cpf: str, cliente_update: ClienteUpdateNome):
    clientes = database.carregar_clientes()
    cliente_encontrado = False
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = True
            break
    
    if not cliente_encontrado:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")
    
    database.atualizar_cliente_nome(cpf, cliente_update.nome)
    
    clientes_atualizado = database.carregar_clientes()
    for cliente in clientes_atualizado:
        if cliente.cpf == cpf:
            return cliente

# EMAIL
@router.patch("/{cpf}/email", response_model = clienteResponse)
def atualizar_cliente_email(cpf: str, cliente_update: ClienteUpdateEmail):
    clientes = database.carregar_clientes()
    cliente_encontrado = False
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = True
            break
    
    if not cliente_encontrado:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")
    
    database.atualizar_cliente_email(cpf, cliente_update.email)
    
    clientes_atualizado = database.carregar_clientes()
    for cliente in clientes_atualizado:
        if cliente.cpf == cpf:
            return cliente

# Rotas DELETE
@router.delete("/{cpf}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_cliente(cpf: str):
    clientes = database.carregar_clientes()
    cliente_encontrado = False
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = True
            break
    
    if not cliente_encontrado:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")
    
    database.deletar_cliente(cpf)


# ===== ROTAS ENDEREÇOS =====

# CREATE - Adicionar endereço ao cliente
@router.post("/{cpf}/enderecos", response_model = ClienteComEnderecosResponse, status_code = status.HTTP_201_CREATED)
def adicionar_endereco(cpf: str, endereco: EnderecoCreate):
    """Adiciona um novo endereço ao cliente"""
    clientes = database.carregar_clientes()
    cliente_encontrado = None
    
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = cliente
            break
    
    if not cliente_encontrado:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")
    
    novo_endereco = Endereco(
        cep = endereco.cep,
        numero = endereco.numero,
        cidade = endereco.cidade,
        UF = endereco.UF
    )
    
    cliente_encontrado.endereco.append(novo_endereco)
    database.atualizar_cliente_endereco(cpf, cliente_encontrado.endereco)
    
    return {
        "nome": cliente_encontrado.nome,
        "email": cliente_encontrado.email,
        "cpf": cliente_encontrado.cpf,
        "enderecos": cliente_encontrado.endereco
    }

# READ - Listar endereços do cliente
@router.get("/{cpf}/enderecos", response_model = list[EnderecoResponse])
def listar_enderecos(cpf: str):
    """Lista todos os endereços de um cliente"""
    clientes = database.carregar_clientes()
    
    for cliente in clientes:
        if cliente.cpf == cpf:
            if not cliente.endereco:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não possui endereços cadastrados.")
            return cliente.endereco
    
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")

# UPDATE - Atualizar endereço do cliente
@router.patch("/{cpf}/enderecos/{indice}", response_model = ClienteComEnderecosResponse)
def atualizar_endereco(cpf: str, indice: int, endereco_update: EnderecoUpdate):
    """Atualiza um endereço específico do cliente"""
    clientes = database.carregar_clientes()
    cliente_encontrado = None
    
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = cliente
            break
    
    if not cliente_encontrado:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")
    
    if indice < 0 or indice >= len(cliente_encontrado.endereco):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Índice de endereço inválido.")
    
    endereco = cliente_encontrado.endereco[indice]
    
    if endereco_update.cep is not None:
        endereco.cep = endereco_update.cep
    if endereco_update.numero is not None:
        endereco.numero = endereco_update.numero
    if endereco_update.cidade is not None:
        endereco.cidade = endereco_update.cidade
    if endereco_update.UF is not None:
        endereco.UF = endereco_update.UF
    
    database.atualizar_cliente_endereco(cpf, cliente_encontrado.endereco)
    
    return {
        "nome": cliente_encontrado.nome,
        "email": cliente_encontrado.email,
        "cpf": cliente_encontrado.cpf,
        "enderecos": cliente_encontrado.endereco
    }

# DELETE - Remover endereço do cliente
@router.delete("/{cpf}/enderecos/{indice}", status_code = status.HTTP_204_NO_CONTENT)
def deletar_endereco(cpf: str, indice: int):
    """Remove um endereço específico do cliente"""
    clientes = database.carregar_clientes()
    cliente_encontrado = None
    
    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = cliente
            break
    
    if not cliente_encontrado:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Cliente não encontrado.")
    
    if indice < 0 or indice >= len(cliente_encontrado.endereco):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Índice de endereço inválido.")
    
    cliente_encontrado.endereco.pop(indice)
    database.atualizar_cliente_endereco(cpf, cliente_encontrado.endereco)