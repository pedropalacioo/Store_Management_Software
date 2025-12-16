import sqlite3
import json
from pathlib import Path
from typing import List

from core.cliente import Cliente
from core.endereco import Endereco
from core.produto import Produto
from core.produto_fisico import ProdutoFisico
from core.produto_digital import ProdutoDigital

DB_PATH = Path("db/database.db")


def get_db_path() -> Path:
    """Retorna o caminho do banco de dados."""
    return DB_PATH


#--------------------------------------------------------------
# TABELA DE CLIENTES
#--------------------------------------------------------------

try:

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            cpf TEXT NOT NULL,
            endereco TEXT
        );"""

        cursor.execute(create_table_query)

        conn.commit()

        print("Tabela 'clientes' criada com sucesso(ou já existia).")

        # Garantir que a coluna 'endereco' exista (migração simples)
        cursor.execute("PRAGMA table_info(clientes);")
        cols = [row[1] for row in cursor.fetchall()]
        if 'endereco' not in cols:
            cursor.execute("ALTER TABLE clientes ADD COLUMN endereco TEXT;")
            conn.commit()
            print("Coluna 'endereco' adicionada à tabela 'clientes'.")

except sqlite3.Error as e:
    print(f"Erro no SQLite: {e}")

# CRUD - CREATE
def salvar_cliente(cliente: Cliente) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Converter endereços para JSON
        enderecos_json = json.dumps([
            {
                "cep": endereco.cep,
                "numero": endereco.numero,
                "cidade": endereco.cidade,
                "UF": endereco.UF
            }
            for endereco in cliente.endereco
        ])
        
        insert_query = """
        INSERT INTO clientes (nome, email, cpf, endereco) VALUES (?, ?, ?, ?);
        """
        cursor.execute(insert_query, (cliente.nome, cliente.email, cliente.cpf, enderecos_json))
        conn.commit()
    print("Cliente salvo com sucesso na database.")

# CRUD - READ
def carregar_clientes() -> list[Cliente]:
    clientes = []
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        select_query = "SELECT nome, email, cpf, endereco FROM clientes;"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        conn.commit()

    for row in rows:
        # Converter JSON de volta para lista de Endereco
        enderecos = []
        if row[3]:  # Se houver endereços salvos
            enderecos_data = json.loads(row[3])
            for endereco_data in enderecos_data:
                endereco = Endereco(
                    cep=endereco_data["cep"],
                    numero=endereco_data["numero"],
                    cidade=endereco_data["cidade"],
                    UF=endereco_data["UF"]
                )
                enderecos.append(endereco)
        
        c = Cliente(
            nome = row[0],
            email = row[1],
            cpf = row[2],
            endereco = enderecos
        )
        clientes.append(c)
    return clientes

# CRUD - UPDATE
def atualizar_cliente_nome(cpf: str, novo_nome: str = None) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if novo_nome is not None:
            update_nome_query = "UPDATE clientes SET nome = ? WHERE cpf = ?;"
            cursor.execute(update_nome_query, (novo_nome, cpf))
            conn.commit()
            print(f"Nome do cliente de cpf {cpf} atualizado com sucesso na database.")

def atualizar_cliente_email(cpf: str, novo_email: str = None) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        if novo_email is not None:
            update_email_query = "UPDATE clientes SET email = ? WHERE cpf = ?;"
            cursor.execute(update_email_query, (novo_email, cpf))
            conn.commit()
            print(f"Email do cliente cpf: {cpf} atualizado com sucesso.")

def atualizar_cliente_endereco(cpf: str, enderecos: list) -> None:
    """Atualiza os endereços de um cliente armazenando em JSON"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Converter lista de endereços para JSON
        enderecos_json = json.dumps([
            {
                "cep": endereco.cep,
                "numero": endereco.numero,
                "cidade": endereco.cidade,
                "UF": endereco.UF
            }
            for endereco in enderecos
        ])
        
        update_endereco_query = "UPDATE clientes SET endereco = ? WHERE cpf = ?;"
        cursor.execute(update_endereco_query, (enderecos_json, cpf))
        conn.commit()
        print(f"Endereços do cliente cpf: {cpf} atualizados com sucesso.")
# CRUD - DELETE
def deletar_cliente(cpf: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        delete_query = "DELETE FROM clientes WHERE cpf = ?;"
        cursor.execute(delete_query, (cpf,))
        conn.commit()
        print(f"Cliente de cpf {cpf} deletado com sucesso da database.")


#--------------------------------------------------------------
# TABELA DE PRODUTOS (Single Table Inheritance)
#--------------------------------------------------------------

try:

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco REAL NOT NULL,
            tipo TEXT NOT NULL,
            sku TEXT,
            estoque INTEGER DEFAULT 0,
            peso REAL,
            altura REAL,
            largura REAL,
            profundidade REAL,
            url_download TEXT,
            chave_licenca TEXT
        );"""

        cursor.execute(create_table_query)
        conn.commit()
        print("Tabela 'produtos' criada com sucesso (ou já existia).")
        
        # Migração: adicionar colunas SKU e ESTOQUE se não existirem
        cursor.execute("PRAGMA table_info(produtos);")
        cols = [row[1] for row in cursor.fetchall()]
        if 'sku' not in cols:
            cursor.execute("ALTER TABLE produtos ADD COLUMN sku TEXT;")
            conn.commit()
            print("Coluna 'sku' adicionada à tabela 'produtos'.")
        if 'estoque' not in cols:
            cursor.execute("ALTER TABLE produtos ADD COLUMN estoque INTEGER DEFAULT 0;")
            conn.commit()
            print("Coluna 'estoque' adicionada à tabela 'produtos'.")

except sqlite3.Error as e:
    print(f"Erro no SQLite: {e}")


# CRUD - CREATE
def salvar_produto(produto: Produto) -> None:
    """Salva um produto (físico ou digital) na tabela de produtos"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        if isinstance(produto, ProdutoFisico):
            insert_query = """
            INSERT INTO produtos (nome, descricao, preco, tipo, sku, peso, altura, largura, profundidade) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, (
                produto.nome,
                produto.descricao,
                produto.preco,
                produto.tipo,
                produto.sku,
                produto.peso,
                produto.altura,
                produto.largura,
                produto.profundidade
            ))
        elif isinstance(produto, ProdutoDigital):
            insert_query = """
            INSERT INTO produtos (nome, descricao, preco, tipo, sku, url_download, chave_licenca) 
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
            cursor.execute(insert_query, (
                produto.nome,
                produto.descricao,
                produto.preco,
                produto.tipo,
                produto.sku,
                produto.url_download,
                produto.chave_licenca
            ))
        
        conn.commit()
    print(f"Produto {produto.tipo} '{produto.nome}' salvo com sucesso.")


# CRUD - READ
def carregar_produtos() -> list[Produto]:
    """Carrega todos os produtos (físicos e digitais) da tabela"""
    produtos = []
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        select_query = "SELECT id, nome, descricao, preco, tipo, sku, peso, altura, largura, profundidade, url_download, chave_licenca FROM produtos;"
        cursor.execute(select_query)
        rows = cursor.fetchall()
        conn.commit()

    for row in rows:
        tipo = row[4]
        
        if tipo == "fisico":
            p = ProdutoFisico(
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                peso=row[6],
                altura=row[7],
                largura=row[8],
                profundidade=row[9],
                sku=row[5]
            )
        elif tipo == "digital":
            p = ProdutoDigital(
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                url_download=row[10],
                chave_licenca=row[11],
                sku=row[5]
            )
        
        produtos.append(p)
    return produtos


def buscar_produto_por_nome(nome: str) -> list[Produto]:
    """Busca produtos pelo nome"""
    produtos = []
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        select_query = "SELECT id, nome, descricao, preco, tipo, sku, peso, altura, largura, profundidade, url_download, chave_licenca FROM produtos WHERE nome LIKE ?;"
        cursor.execute(select_query, (f"%{nome}%",))
        rows = cursor.fetchall()
        conn.commit()

    for row in rows:
        tipo = row[4]
        
        if tipo == "fisico":
            p = ProdutoFisico(
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                peso=row[6],
                altura=row[7],
                largura=row[8],
                profundidade=row[9],
                sku=row[5]
            )
        elif tipo == "digital":
            p = ProdutoDigital(
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                url_download=row[10],
                chave_licenca=row[11],
                sku=row[5]
            )
        
        produtos.append(p)
    return produtos


# CRUD - UPDATE
def atualizar_produto(id: int, nome: str = None, descricao: str = None, preco: float = None) -> None:
    """Atualiza informações básicas de um produto"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        if nome is not None:
            cursor.execute("UPDATE produtos SET nome = ? WHERE id = ?;", (nome, id))
            conn.commit()
        
        if descricao is not None:
            cursor.execute("UPDATE produtos SET descricao = ? WHERE id = ?;", (descricao, id))
            conn.commit()
        
        if preco is not None:
            cursor.execute("UPDATE produtos SET preco = ? WHERE id = ?;", (preco, id))
            conn.commit()
    
    print(f"Produto ID {id} atualizado com sucesso.")


def atualizar_produto_fisico_dimensoes(id: int, peso: float = None, altura: float = None, largura: float = None, profundidade: float = None) -> None:
    """Atualiza dimensões de um produto físico"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        if peso is not None:
            cursor.execute("UPDATE produtos SET peso = ? WHERE id = ?;", (peso, id))
            conn.commit()

        if altura is not None:
            cursor.execute("UPDATE produtos SET altura = ? WHERE id = ?;", (altura, id))
            conn.commit()

        if largura is not None:
            cursor.execute("UPDATE produtos SET largura = ? WHERE id = ?;", (largura, id))
            conn.commit()

        if profundidade is not None:
            cursor.execute("UPDATE produtos SET profundidade = ? WHERE id = ?;", (profundidade, id))
            conn.commit()

    print(f"Dimensões do produto físico ID {id} atualizadas com sucesso.")


def atualizar_produto_digital_url(id: int, url_download: str = None, chave_licenca: str = None) -> None:
    """Atualiza URL e chave de licença de um produto digital"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        if url_download is not None:
            cursor.execute("UPDATE produtos SET url_download = ? WHERE id = ?;", (url_download, id))
            conn.commit()

        if chave_licenca is not None:
            cursor.execute("UPDATE produtos SET chave_licenca = ? WHERE id = ?;", (chave_licenca, id))
            conn.commit()

    print(f"Dados do produto digital ID {id} atualizados com sucesso.")


# CRUD - DELETE
def deletar_produto(id: int) -> None:
    """Deleta um produto da tabela por ID"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        delete_query = "DELETE FROM produtos WHERE id = ?;"
        cursor.execute(delete_query, (id,))
        conn.commit()

    print(f"Produto ID {id} deletado com sucesso.")


def deletar_produto_por_sku(sku: str) -> None:
    """Deleta um produto da tabela por SKU"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        delete_query = "DELETE FROM produtos WHERE sku = ?;"
        cursor.execute(delete_query, (sku,))
        conn.commit()

    print(f"Produto SKU {sku} deletado com sucesso.")


# Helper functions para testes
def salvar_cupom(cupom) -> int:
    """Salva um cupom no banco (função helper para testes)."""
    from core.cupom import Cupom
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Criar tabela de cupons se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cupons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT NOT NULL UNIQUE,
                percentual_desconto REAL NOT NULL,
                valor_minimo_compra REAL NOT NULL,
                ativo BOOLEAN NOT NULL DEFAULT 1
            )
        """)
        
        cursor.execute(
            "INSERT INTO cupons (codigo, percentual_desconto, valor_minimo_compra, ativo) VALUES (?, ?, ?, ?)",
            (cupom.codigo, cupom.percentual_desconto, cupom.valor_minimo_compra, cupom.ativo)
        )
        conn.commit()
        return cursor.lastrowid


def salvar_endereco(endereco) -> int:
    """Salva um endereço no banco (função helper para testes)."""
    from core.endereco import Endereco
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Criar tabela de endereços se não existir
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enderecos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cep TEXT NOT NULL,
                numero INTEGER NOT NULL,
                cidade TEXT NOT NULL,
                uf TEXT NOT NULL
            )
        """)
        
        cursor.execute(
            "INSERT INTO enderecos (cep, numero, cidade, uf) VALUES (?, ?, ?, ?)",
            (endereco.cep, endereco.numero, endereco.cidade, endereco.uf)
        )
        conn.commit()
        return cursor.lastrowid
