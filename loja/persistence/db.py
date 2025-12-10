# File para persistência de dados em SQLite
#precisa ser revisado!!!

# db.py
from __future__ import annotations

import sqlite3
import datetime
from pathlib import Path
from typing import List, Optional
import json

from loja.src.produto import Produto
from loja.src.cliente import Cliente
from loja.src.pedido import Pedido
from loja.src.item_pedido import ItemPedido
from loja.src.cupom import Cupom

# Caminho do arquivo do banco
DB_PATH = Path(__file__).resolve().parent / "loja.db"

# adaptar datetime.date/datetime para SQLite e reconverter ao ler
sqlite3.register_adapter(datetime.date, lambda d: d.isoformat())
sqlite3.register_adapter(datetime.datetime, lambda dt: dt.isoformat(sep=' '))
sqlite3.register_converter("DATE", lambda b: datetime.date.fromisoformat(b.decode()))
sqlite3.register_converter("TIMESTAMP", lambda b: datetime.datetime.fromisoformat(b.decode()))

# ========== CONEXÃO ==========

def get_connection() -> sqlite3.Connection:
    """
    Abre uma conexão com o SQLite.
    row_factory = sqlite3.Row permite acessar colunas por nome.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# Criação de tabelas

def init_db() -> None:
    """
    Cria as tabelas básicas se ainda não existirem.
    Rode uma vez no início da aplicação (ex.: comando 'loja init-db').
    """
    ddl = """
    CREATE TABLE IF NOT EXISTS produtos (
        sku INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        categoria TEXT,
        preco REAL NOT NULL,
        estoque INTEGER NOT NULL,
        ativo INTEGER NOT NULL CHECK (ativo IN (0,1))
    );

    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        cpf TEXT NOT NULL UNIQUE
    );

    -- Endereços podem ser modelados em tabela própria ou JSON;
    -- aqui deixo uma tabela simples para futuro uso (opcional)
    CREATE TABLE IF NOT EXISTS enderecos (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        cep TEXT NOT NULL,
        cidade TEXT NOT NULL,
        uf TEXT NOT NULL,
        logradouro TEXT NOT NULL,
        numero TEXT NOT NULL,
        complemento TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
    );

    CREATE TABLE IF NOT EXISTS cupons (
        codigo TEXT PRIMARY KEY,
        tipo TEXT NOT NULL,
        valor REAL NOT NULL,
        data_validade TEXT,
        uso_maximo INTEGER NOT NULL,
        usos_realizados INTEGER NOT NULL,
        categorias_elegiveis TEXT
    );

    CREATE TABLE IF NOT EXISTS pedidos (
        id INTEGER PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        subtotal REAL NOT NULL,
        descontos REAL NOT NULL,
        valor_frete REAL NOT NULL,
        total REAL NOT NULL,
        criado_em TEXT NOT NULL,
        pago_em TEXT,
        enviado_em TEXT,
        entregue_em TEXT,
        cancelado_em TEXT,
        codigo_rastreio TEXT,
        endereco_entrega_json TEXT NOT NULL,
        cupom_codigo TEXT,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id),
        FOREIGN KEY (cupom_codigo) REFERENCES cupons(codigo)
    );

    CREATE TABLE IF NOT EXISTS itens_pedido (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pedido_id INTEGER NOT NULL,
        sku TEXT NOT NULL,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario REAL NOT NULL,
        FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
    );
    """

    conn = get_connection()
    try:
        conn.executescript(ddl)
        conn.commit()
    finally:
        conn.close()


# HELPERS GERAIS

def _dt_to_str(dt: Optional[datetime.datetime]) -> Optional[str]:
    if dt is None:
        return None
    return dt.isoformat(timespec="seconds")


def _str_to_dt(s: Optional[str]) -> Optional[datetime.datetime]:
    if not s:
        return None
    return datetime.fromisoformat(s)


# ====================================
#   PRODUTO
# ====================================

def salvar_produto(produto: Produto) -> None:
    """
    Insere ou atualiza um produto no banco.
    Usa sku como chave primária.
    """
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO produtos (sku, nome, categoria, preco, estoque, ativo)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(sku) DO UPDATE SET
                nome = excluded.nome,
                categoria = excluded.categoria,
                preco = excluded.preco,
                estoque = excluded.estoque,
                ativo = excluded.ativo
            """,
            (
                produto.sku,
                produto.nome,
                produto.categoria,
                produto.preco,
                produto.estoque,
                1 if produto.ativo else 0,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def listar_produtos() -> List[Produto]:
    """
    Retorna todos os produtos do banco como objetos Produto.
    """
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT sku, nome, categoria, preco, estoque, ativo FROM produtos"
        )
        rows = cur.fetchall()
    finally:
        conn.close()

    produtos: List[Produto] = []
    for row in rows:
        p = Produto(
            sku=row["sku"],
            nome=row["nome"],
            categoria=row["categoria"],
            preco=row["preco"],
            estoque=row["estoque"],
            ativo=bool(row["ativo"]),
        )
        produtos.append(p)
    return produtos


def buscar_produto_por_sku(sku: int) -> Optional[Produto]:
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT sku, nome, categoria, preco, estoque, ativo FROM produtos WHERE sku = ?",
            (sku,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    return Produto(
        sku=row["sku"],
        nome=row["nome"],
        categoria=row["categoria"],
        preco=row["preco"],
        estoque=row["estoque"],
        ativo=bool(row["ativo"]),
    )


# ====================================
#   CLIENTE (básico)
# ====================================

def salvar_cliente(cliente: Cliente) -> None:
    """
    Insere ou atualiza um cliente.
    Não estou persistindo endereços aqui para manter simples;
    você pode depois criar funções salvar_endereco() etc.
    """
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO clientes (id, nome, email, cpf)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                nome = excluded.nome,
                email = excluded.email,
                cpf = excluded.cpf
            """,
            (cliente.id, cliente.nome, cliente.email, cliente.cpf),
        )
        conn.commit()
    finally:
        conn.close()


def listar_clientes() -> List[Cliente]:
    conn = get_connection()
    try:
        cur = conn.execute("SELECT id, nome, email, cpf FROM clientes")
        rows = cur.fetchall()
    finally:
        conn.close()

    clientes: List[Cliente] = []
    for row in rows:
        # Aqui estou assumindo que o construtor aceita endereco=None
        c = Cliente(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            cpf=row["cpf"],
            endereco=None,
        )
        clientes.append(c)
    return clientes


def buscar_cliente_por_id(cliente_id: int) -> Optional[Cliente]:
    conn = get_connection()
    try:
        cur = conn.execute(
            "SELECT id, nome, email, cpf FROM clientes WHERE id = ?",
            (cliente_id,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    return Cliente(
        id=row["id"],
        nome=row["nome"],
        email=row["email"],
        cpf=row["cpf"],
        endereco=None,
    )


# ====================================
#   CUPOM
# ====================================

def salvar_cupom(cupom: Cupom) -> None:
    """
    Salva ou atualiza um cupom.
    categorias_elegiveis vai como JSON em texto.
    data_validade vai em ISO (YYYY-MM-DD).
    """
    categorias_json = (
        json.dumps(cupom.categorias_elegiveis, ensure_ascii=False)
        if cupom.categorias_elegiveis is not None
        else None
    )
    data_validade_str = (
        cupom.data_validade.isoformat() if cupom.data_validade is not None else None
    )

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO cupons (
                codigo, tipo, valor, data_validade,
                uso_maximo, usos_realizados, categorias_elegiveis
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(codigo) DO UPDATE SET
                tipo = excluded.tipo,
                valor = excluded.valor,
                data_validade = excluded.data_validade,
                uso_maximo = excluded.uso_maximo,
                usos_realizados = excluded.usos_realizados,
                categorias_elegiveis = excluded.categorias_elegiveis
            """,
            (
                cupom.codigo,
                cupom.tipo,
                cupom.valor,
                data_validade_str,
                cupom.uso_maximo,
                cupom.usos_realizados,
                categorias_json,
            ),
        )
        conn.commit()
    finally:
        conn.close()


def buscar_cupom_por_codigo(codigo: str) -> Optional[Cupom]:
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT codigo, tipo, valor, data_validade,
                   uso_maximo, usos_realizados, categorias_elegiveis
            FROM cupons
            WHERE codigo = ?
            """,
            (codigo,),
        )
        row = cur.fetchone()
    finally:
        conn.close()

    if row is None:
        return None

    data_validade = (
        datetime.fromisoformat(row["data_validade"]).date()
        if row["data_validade"]
        else None
    )
    categorias = (
        json.loads(row["categorias_elegiveis"])
        if row["categorias_elegiveis"]
        else None
    )

    return Cupom(
        codigo=row["codigo"],
        tipo=row["tipo"],
        valor=row["valor"],
        data_validade=data_validade,
        uso_maximo=row["uso_maximo"],
        usos_realizados=row["usos_realizados"],
        categ_elegiveis=categorias,
    )


# ====================================
#   PEDIDO + ITENS
# ====================================

def salvar_pedido(pedido: Pedido) -> None:
    """
    Salva ou atualiza um pedido + seus itens.
    - Usa pedido.id como chave primária.
    - Sempre apaga os itens antigos e insere os atuais.
    """

    endereco_json = json.dumps(
        getattr(pedido, "endereco_entrega", None),
        default=lambda o: getattr(o, "__dict__", str(o)),
        ensure_ascii=False,
    )

    cupom_codigo = pedido.cupom.codigo if pedido.cupom is not None else None

    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO pedidos (
                id, cliente_id, status,
                subtotal, descontos, valor_frete, total,
                criado_em, pago_em, enviado_em, entregue_em, cancelado_em,
                codigo_rastreio, endereco_entrega_json, cupom_codigo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                cliente_id = excluded.cliente_id,
                status = excluded.status,
                subtotal = excluded.subtotal,
                descontos = excluded.descontos,
                valor_frete = excluded.valor_frete,
                total = excluded.total,
                criado_em = excluded.criado_em,
                pago_em = excluded.pago_em,
                enviado_em = excluded.enviado_em,
                entregue_em = excluded.entregue_em,
                cancelado_em = excluded.cancelado_em,
                codigo_rastreio = excluded.codigo_rastreio,
                endereco_entrega_json = excluded.endereco_entrega_json,
                cupom_codigo = excluded.cupom_codigo
            """,
            (
                pedido.id,
                pedido.cliente.id,
                pedido.status,
                pedido.subtotal,
                pedido.descontos,
                pedido.valor_frete,
                pedido.total,
                _dt_to_str(pedido.criado_em),
                _dt_to_str(pedido.pago_em),
                _dt_to_str(pedido.enviado_em),
                _dt_to_str(pedido.entregue_em),
                _dt_to_str(pedido.cancelado_em),
                pedido.codigo_rastreio,
                endereco_json,
                cupom_codigo,
            ),
        )

        # Apaga itens antigos e insere os atuais
        conn.execute(
            "DELETE FROM itens_pedido WHERE pedido_id = ?",
            (pedido.id,),
        )

        for item in pedido.itens:
            conn.execute(
                """
                INSERT INTO itens_pedido (
                    pedido_id, sku, nome, quantidade, preco_unitario
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    pedido.id,
                    item.sku,
                    item.nome,
                    item.quantidade,
                    item.preco_unitario(),  # no seu código é método, não @property
                ),
            )

        conn.commit()
    finally:
        conn.close()


def _carregar_itens_pedido(conn: sqlite3.Connection, pedido_id: int) -> List[ItemPedido]:
    cur = conn.execute(
        """
        SELECT sku, nome, quantidade, preco_unitario
        FROM itens_pedido
        WHERE pedido_id = ?
        """,
        (pedido_id,),
    )
    rows = cur.fetchall()

    itens: List[ItemPedido] = []
    for row in rows:
        item = ItemPedido(
            sku=row["sku"],
            nome=row["nome"],
            quantidade=row["quantidade"],
            preco_unitario=row["preco_unitario"],
        )
        itens.append(item)
    return itens


def listar_pedidos() -> List[Pedido]:
    """
    Carrega todos os pedidos do banco.
    Observação: para manter a compatibilidade e simplicidade, o frete é
    reconstruído como None (o valor de frete já está persistido em valor_frete).
    Se quiser, você pode recalcular com Frete.from_cliente(cliente).
    """
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT
                id, cliente_id, status,
                subtotal, descontos, valor_frete, total,
                criado_em, pago_em, enviado_em, entregue_em, cancelado_em,
                codigo_rastreio, endereco_entrega_json, cupom_codigo
            FROM pedidos
            """
        )
        rows = cur.fetchall()

        pedidos: List[Pedido] = []

        for row in rows:
            cliente = buscar_cliente_por_id(row["cliente_id"])
            if cliente is None:
                # Se der algum problema, pula
                continue

            endereco_entrega = None
            if row["endereco_entrega_json"]:
                try:
                    endereco_entrega = json.loads(row["endereco_entrega_json"])
                except json.JSONDecodeError:
                    endereco_entrega = None

            # Cupom é opcional
            cupom = None
            if row["cupom_codigo"]:
                cupom = buscar_cupom_por_codigo(row["cupom_codigo"])

            itens = _carregar_itens_pedido(conn, row["id"])

            # frete = None para simplificar; valor já está em valor_frete
            pedido = Pedido(
                cliente=cliente,
                itens=itens,
                frete=None,
                cupom=cupom,
                endereco_entrega=endereco_entrega,
                status=row["status"],
                criado_em=_str_to_dt(row["criado_em"]),
            )

            # Ajusta campos que o __init__ calculou de novo
            pedido.subtotal = row["subtotal"]
            pedido.descontos = row["descontos"]
            pedido.valor_frete = row["valor_frete"]
            pedido.total = row["total"]

            pedido.pago_em = _str_to_dt(row["pago_em"])
            pedido.enviado_em = _str_to_dt(row["enviado_em"])
            pedido.entregue_em = _str_to_dt(row["entregue_em"])
            pedido.cancelado_em = _str_to_dt(row["cancelado_em"])
            pedido.codigo_rastreio = row["codigo_rastreio"]

            pedidos.append(pedido)

        return pedidos
    finally:
        conn.close()
