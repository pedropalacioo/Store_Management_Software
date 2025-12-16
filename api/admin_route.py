"""
Router para operações administrativas.
Endpoints para resetar e limpar o banco de dados.
"""

from fastapi import APIRouter, HTTPException, status
import sqlite3
from pathlib import Path

DB_PATH = Path("db/database.db")

router = APIRouter(
    prefix="/admin",
    tags=["Administração"],
)


@router.delete("/limpar/produtos", status_code=status.HTTP_204_NO_CONTENT)
def limpar_produtos():
    """
    Deleta todos os produtos do banco de dados.
    AVISO: Esta operação não pode ser desfeita!
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos;")
            conn.commit()
        print("Todos os produtos foram deletados.")
        return None
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao limpar produtos: {str(e)}"
        )


@router.delete("/limpar/clientes", status_code=status.HTTP_204_NO_CONTENT)
def limpar_clientes():
    """
    Deleta todos os clientes do banco de dados.
    AVISO: Esta operação não pode ser desfeita!
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes;")
            conn.commit()
        print("Todos os clientes foram deletados.")
        return None
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao limpar clientes: {str(e)}"
        )


@router.delete("/resetar-banco", status_code=status.HTTP_204_NO_CONTENT)
def resetar_banco():
    """
    Reseta completamente o banco de dados, deletando todas as tabelas e recriando-as vazias.
    AVISO: Esta operação não pode ser desfeita! Todos os dados serão perdidos.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Deletar todas as tabelas
            cursor.execute("DROP TABLE IF EXISTS clientes;")
            cursor.execute("DROP TABLE IF EXISTS produtos;")
            conn.commit()
            
            # Recriar tabelas vazias
            # Tabela de clientes
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                cpf TEXT NOT NULL,
                endereco TEXT
            );""")
            
            # Tabela de produtos
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT NOT NULL,
                preco REAL NOT NULL,
                tipo TEXT NOT NULL,
                sku TEXT,
                peso REAL,
                altura REAL,
                largura REAL,
                profundidade REAL,
                url_download TEXT,
                chave_licenca TEXT
            );""")
            
            conn.commit()
        
        print("Banco de dados foi resetado com sucesso.")
        return None
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao resetar banco de dados: {str(e)}"
        )


@router.get("/status")
def status_banco():
    """
    Retorna informações sobre o estado do banco de dados.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            
            # Contar clientes
            cursor.execute("SELECT COUNT(*) FROM clientes;")
            total_clientes = cursor.fetchone()[0]
            
            # Contar produtos
            cursor.execute("SELECT COUNT(*) FROM produtos;")
            total_produtos = cursor.fetchone()[0]
            
            # Contar produtos por tipo
            cursor.execute("SELECT tipo, COUNT(*) FROM produtos GROUP BY tipo;")
            produtos_por_tipo = dict(cursor.fetchall())
        
        return {
            "total_clientes": total_clientes,
            "total_produtos": total_produtos,
            "produtos_por_tipo": produtos_por_tipo
        }
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter status: {str(e)}"
        )
