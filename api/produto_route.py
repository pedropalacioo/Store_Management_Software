from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel

import db.database as database
from core.produto_digital import ProdutoDigital
from core.produto_fisico import ProdutoFisico
from services.services_database import validar_sku_unico, ValidacaoDatabaseError

router = APIRouter(
    prefix = "/produtos",
    tags = ["Produtos"],
)

# Modelos Pydantic

# Produto Físico
class ProdutoFisicoCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    peso: float
    altura: float
    largura: float
    profundidade: float
    sku: str | None = None

class ProdutoFisicoUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = None
    peso: float | None = None
    altura: float | None = None
    largura: float | None = None
    profundidade: float | None = None

class ProdutoFisicoResponse(BaseModel):
    nome: str
    descricao: str
    preco: float
    tipo: str
    sku: str | None = None
    peso: float
    altura: float
    largura: float
    profundidade: float

# Produto Digital
class ProdutoDigitalCreate(BaseModel):
    nome: str
    descricao: str
    preco: float
    url_download: str
    chave_licenca: str | None = None
    sku: str | None = None

class ProdutoDigitalUpdate(BaseModel):
    nome: str | None = None
    descricao: str | None = None
    preco: float | None = None
    url_download: str | None = None
    chave_licenca: str | None = None

class ProdutoDigitalResponse(BaseModel):
    nome: str
    descricao: str
    preco: float
    tipo: str
    sku: str | None = None
    url_download: str
    chave_licenca: str | None = None

# Resposta genérica
class ProdutoResponse(BaseModel):
    nome: str
    descricao: str
    preco: float
    tipo: str
    sku: str | None = None

# CREATE

@router.post("/fisico", response_model=ProdutoFisicoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto_fisico(produto: ProdutoFisicoCreate):
    """Cria um novo produto físico"""
    # Validar SKU único se fornecido
    if produto.sku:
        try:
            validar_sku_unico(produto.sku)
        except ValidacaoDatabaseError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    novo_produto = ProdutoFisico(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        peso=produto.peso,
        altura=produto.altura,
        largura=produto.largura,
        profundidade=produto.profundidade,
        sku=produto.sku,
    )
    database.salvar_produto(novo_produto)
    return novo_produto

@router.post("/digital", response_model=ProdutoDigitalResponse, status_code=status.HTTP_201_CREATED)
def criar_produto_digital(produto: ProdutoDigitalCreate):
    """Cria um novo produto digital"""
    # Validar SKU único se fornecido
    if produto.sku:
        try:
            validar_sku_unico(produto.sku)
        except ValidacaoDatabaseError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
    
    novo_produto = ProdutoDigital(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        url_download=produto.url_download,
        chave_licenca=produto.chave_licenca,
        sku=produto.sku,
    )
    database.salvar_produto(novo_produto)
    return novo_produto

# READ

@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos():
    """Lista todos os produtos"""
    produtos = database.carregar_produtos()
    return produtos

@router.get("/buscar/{nome}", response_model=list[ProdutoResponse])
def buscar_produtos_por_nome(nome: str):
    """Busca produtos pelo nome"""
    produtos = database.buscar_produto_por_nome(nome)
    
    if not produtos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum produto encontrado com esse nome."
        )
    
    return produtos

@router.get("/tipo/fisico", response_model=list[ProdutoFisicoResponse])
def listar_produtos_fisicos():
    """Lista apenas produtos físicos"""
    todos_produtos = database.carregar_produtos()
    produtos_fisicos = [p for p in todos_produtos if isinstance(p, ProdutoFisico)]
    
    if not produtos_fisicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum produto físico encontrado."
        )
    
    return produtos_fisicos

@router.get("/tipo/digital", response_model=list[ProdutoDigitalResponse])
def listar_produtos_digitais():
    """Lista apenas produtos digitais"""
    todos_produtos = database.carregar_produtos()
    produtos_digitais = [p for p in todos_produtos if isinstance(p, ProdutoDigital)]
    
    if not produtos_digitais:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum produto digital encontrado."
        )
    
    return produtos_digitais

# ROTAS UPDATE

@router.patch("/{id}/nome")
def atualizar_nome_produto(id: int, nome: str):
    """Atualiza o nome de um produto"""
    database.atualizar_produto(id, nome=nome)
    return {"mensagem": "Nome atualizado com sucesso"}

@router.patch("/{id}/descricao")
def atualizar_descricao_produto(id: int, descricao: str):
    """Atualiza a descrição de um produto"""
    database.atualizar_produto(id, descricao=descricao)
    return {"mensagem": "Descrição atualizada com sucesso"}

@router.patch("/{id}/preco")
def atualizar_preco_produto(id: int, preco: float):
    """Atualiza o preço de um produto"""
    if preco < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Preço não pode ser negativo."
        )
    
    database.atualizar_produto(id, preco=preco)
    return {"mensagem": "Preço atualizado com sucesso"}

@router.patch("/{id}/dimensoes")
def atualizar_dimensoes_produto(id: int, peso: float = None, altura: float = None, largura: float = None, profundidade: float = None):
    """Atualiza as dimensões de um produto físico"""
    database.atualizar_produto_fisico_dimensoes(id, peso, altura, largura, profundidade)
    return {"mensagem": "Dimensões atualizadas com sucesso"}

@router.patch("/{id}/url")
def atualizar_url_produto(id: int, url_download: str = None, chave_licenca: str = None):
    """Atualiza URL e chave de licença de um produto digital"""
    database.atualizar_produto_digital_url(id, url_download, chave_licenca)
    return {"mensagem": "Dados do produto digital atualizados com sucesso"}

# ROTAS DELETE

@router.delete("/por-id/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto_por_id(id: int):
    """Deleta um produto pelo ID"""
    database.deletar_produto(id)
    return None


@router.delete("/por-sku/{sku}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto_por_sku(sku: str):
    """Deleta um produto pelo SKU"""
    database.deletar_produto_por_sku(sku)
    return None

