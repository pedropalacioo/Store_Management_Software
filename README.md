# Store Management Software
*Projeto da cadeira de Programação Orientada à Objetos do curso de Engenharia de Software*

**Aluno: Pedro Yan Alcantara Palacio**
*Engenharia de Software - Universidade Federal do Cariri*

----

## 1. Objetivo do projeto: 
Desenvolver um **sistema simplificado de gerenciamento de loja virtual**, aplicando conceitos essenciais de **Programação Orientada a Objetos**:

----

## 2. UML Textual com estrutura das Classes (Implementadas):

| **Classe** | **Atributos Principais** | **Métodos Principais** |
|-----------|---------------------------|-------------------------|
| **Produto** (Abstract) | `sku`, `nome`, `descricao`, `_preco`, `_estoque`, `tipo`, `_categoria`, `ativo` | `preco/get/set`, `estoque/get/set`, `sku/get/set`, `categoria/get/set`, `ativo/get/set`, `__str__()` |
| **ProdutoFisico** | herda `Produto` + `_peso`, `_altura`, `_largura`, `_profundidade` | herda de Produto + `peso/get/set`, `altura/get/set`, `largura/get/set`, `profundidade/get/set` |
| **ProdutoDigital** | herda `Produto` + `_url_download`, `_chave_licenca` | herda de Produto + `url_download/get/set`, `chave_licenca/get/set`, `gerar_chave_licenca()` |
| **Cliente** | `nome`, `_email`, `_cpf`, `endereco: list[Endereco]` | `email/get/set`, `cpf/get/set`, `__eq__()` |
| **Endereco** | `_cep`, `_numero`, `_cidade`, `_UF` | `cep/get/set`, `numero/get/set`, `cidade/get/set`, `UF/get/set`, `__str__()` |
| **Carrinho** | `cliente: Cliente`, `itens: list[ItemCarrinho]`, `criado_em`, `atualizado_em`, `ativo` | `adicionar_item()`, `remover_item()`, `subtotal()`, `__len__()` |
| **ItemCarrinho** | `produto: Produto`, `_quantidade` | `quantidade/get/set`, `subtotal()` |
| **Pedido** | `cliente: Cliente`, `itens: list[ItemPedido]`, `cupom`, `endereco_entrega`, `status`, `criado_em`, `pago_em`, `cancelado_em` | `criar_de_carrinho()`, `calcular_subtotal()`, `aplicar_cupom()`, `cancelar()` |
| **ItemPedido** | `produto: Produto`, `quantidade`, `preco_unitario` | `total_item()` |
| **Pagamento** | `_pedido: Pedido`, `_valor`, `_metodo`, `_numero_parcelas`, `_data_pagamento`, `_status` | `valor/get/set`, `metodo/get/set`, `numero_parcelas/get/set`, `confirmar()`, `estornar()` |
| **Cupom** | `_codigo`, `_percentual_desconto`, `_valor_minimo_compra`, `_ativo`, `_data_criacao` | `codigo/get/set`, `percentual_desconto/get/set`, `validar()`, `calcular_desconto()`, `aplicar_desconto()` |
| **Frete** | `cep_origem`, `cep_destino`, `peso_kg`, `dimensoes`, `transportadora` | `calcular_frete()`, `consultar_rastreamento()` |

----

## 3. Estrutura das Classes (Implementadas):

Abaixo estão as classes do domínio da loja virtual, conforme implementadas no projeto.

---

### Classe `Produto` (Classe Base Abstrata)

- **Responsabilidade**: representar um produto vendável (base para produtos físicos e digitais).
- **Atributos principais**
  - `sku: str | None` — identificador único (opcional).
  - `nome: str` — nome do produto.
  - `descricao: str` — descrição do produto.
  - `_preco: float` — preço (> 0), acessado via `@property`.
  - `_estoque: int` — quantidade em estoque (≥ 0), acessado via `@property`.
  - `tipo: str` — tipo do produto (`"fisico"` ou `"digital"`).
  - `_categoria: str` — categoria (padrão: `"Geral"`), acessada via `@property`.
  - `_ativo: bool` — disponível para venda (padrão: `True`), acessado via `@property`.
- **Métodos principais**
  - `preco` (getter/setter) — valida preço > 0.
  - `estoque` (getter/setter) — valida estoque ≥ 0.
  - `sku` (getter/setter) — valida SKU não-vazio (se fornecido).
  - `categoria` (getter/setter) — valida categoria não-vazia.
  - `ativo` (getter/setter) — alterna disponibilidade.
  - `__str__()` — representação amigável.
- **Implementação**: Classe não-instanciável (uso via subclasses).

---

### Classe `ProdutoFisico` (Subclasse de `Produto`)

- **Responsabilidade**: produtos físicos com dimensões e peso.
- **Atributos principais**
  - Herda todos de `Produto`.
  - `_peso: float` — peso em kg (> 0), acessado via `@property`.
  - `_altura: float` — altura em cm (> 0), acessado via `@property`.
  - `_largura: float` — largura em cm (> 0), acessado via `@property`.
  - `_profundidade: float` — profundidade em cm (> 0), acessado via `@property`.
- **Métodos principais**
  - Herda todos de `Produto`.
  - `peso`, `altura`, `largura`, `profundidade` (getters/setters) — validações de valores > 0.
- **Validações**: Dimensões e peso devem ser positivos.

---

### Classe `ProdutoDigital` (Subclasse de `Produto`)

- **Responsabilidade**: produtos digitais com URL e licença.
- **Atributos principais**
  - Herda todos de `Produto`.
  - `_url_download: str` — URL para download (não-vazia).
  - `_chave_licenca: str | None` — chave de licença (opcional).
- **Métodos principais**
  - Herda todos de `Produto`.
  - `url_download` (getter/setter) — valida URL não-vazia.
  - `chave_licenca` (getter/setter) — valida chave se fornecida.
  - `gerar_chave_licenca() -> str` — gera chave aleatória de 16 caracteres.
- **Validações**: URL não pode ser vazia.

---

### Classe `Cliente`

- **Responsabilidade**: representar um cliente da loja.
- **Atributos principais**
  - `nome: str` — nome do cliente.
  - `_email: str` — email validado, acessado via `@property`.
  - `_cpf: str` — CPF validado, acessado via `@property`.
  - `endereco: list[Endereco]` — lista de endereços cadastrados.
- **Métodos principais**
  - `nome` (getter/setter) — valida string não-vazia.
  - `email` (getter/setter) — valida formato de email.
  - `cpf` (getter/setter) — valida formato e algoritmo de CPF.
  - `__eq__(other)` — compara por CPF.
  - `__str__()` — representação amigável.
- **Validações**: Email válido, CPF válido (com validação de dígitos).

---

### Classe `Endereco`

- **Responsabilidade**: representar um endereço de entrega.
- **Atributos principais**
  - `_cep: str` — CEP validado, acessado via `@property`.
  - `_numero: int` — número do endereço (≥ 1), acessado via `@property`.
  - `_cidade: str` — cidade, acessada via `@property`.
  - `_UF: str` — unidade federativa (2 letras), acessada via `@property`.
- **Métodos principais**
  - `cep`, `numero`, `cidade`, `UF` (getters/setters) — com validações.
  - `__str__()` — retorna endereço formatado.
- **Validações**: CEP e UF com formato específico, número > 0.

---

### Classe `Carrinho`

- **Responsabilidade**: representar o carrinho de compras.
- **Atributos principais**
  - `cliente: Cliente` — cliente associado.
  - `itens: list[ItemCarrinho]` — itens no carrinho.
  - `criado_em: datetime` — data de criação.
  - `atualizado_em: datetime` — última atualização.
  - `ativo: bool` — indica se carrinho está ativo.
- **Métodos principais**
  - `adicionar_item()` — adiciona item ao carrinho.
  - `remover_item()` — remove item do carrinho.
  - `subtotal() -> float` — soma dos subtotais.
  - `__len__()` — quantidade total de itens.
- **Relacionamentos**: Pertence a um cliente, contém múltiplos `ItemCarrinho`.

---

### Classe `ItemCarrinho`

- **Responsabilidade**: representar um item no carrinho.
- **Atributos principais**
  - `produto: Produto` — referência ao produto.
  - `_quantidade: int` — quantidade (≥ 1), acessada via `@property`.
- **Métodos principais**
  - `quantidade` (getter/setter) — valida quantidade ≥ 1.
  - `subtotal() -> float` — quantidade × preço do produto.
- **Validações**: Quantidade deve ser ≥ 1.

---

### Classe `Pedido`

- **Responsabilidade**: representar um pedido efetivado.
- **Atributos principais**
  - `cliente: Cliente` — cliente que fez o pedido.
  - `itens: list[ItemPedido]` — itens do pedido.
  - `cupom: Cupom | None` — cupom aplicado (opcional).
  - `endereco_entrega: Endereco` — endereço de entrega.
  - `status: str` — status do pedido (`"CRIADO"`, `"PAGO"`, `"CANCELADO"`).
  - `criado_em: datetime` — data de criação.
  - `pago_em: datetime | None` — data do pagamento (se pago).
  - `cancelado_em: datetime | None` — data do cancelamento (se cancelado).
- **Métodos principais**
  - `criar_de_carrinho()` — cria pedido a partir de carrinho.
  - `calcular_subtotal() -> float` — soma dos itens.
  - `aplicar_cupom()` — aplica desconto de cupom.
  - `cancelar()` — cancela o pedido.
- **Relacionamentos**: Contém múltiplos `ItemPedido`, associado a um `Cliente` e `Endereco`.

---

### Classe `ItemPedido`

- **Responsabilidade**: representar um item faturado.
- **Atributos principais**
  - `produto: Produto` — referência ao produto.
  - `quantidade: int` — quantidade comprada.
  - `preco_unitario: float` — preço no momento do pedido.
- **Métodos principais**
  - `total_item() -> float` — quantidade × preço_unitario.
- **Relacionamentos**: Pertence a um `Pedido`.

---

### Classe `Pagamento`

- **Responsabilidade**: representar um pagamento de pedido.
- **Atributos principais**
  - `_pedido: Pedido` — pedido associado, acessado via `@property`.
  - `_valor: float` — valor do pagamento (> 0), acessado via `@property`.
  - `_metodo: str` — forma de pagamento (`"PIX"`, `"CREDITO"`, `"DEBITO"`), acessado via `@property`.
  - `_numero_parcelas: int` — número de parcelas (1-12), acessado via `@property`.
  - `_data_pagamento: datetime` — data do pagamento, acessada via `@property`.
  - `_status: str` — status (`"PENDENTE"`, `"CONFIRMADO"`, `"CANCELADO"`), acessado via `@property`.
- **Métodos principais**
  - `valor`, `metodo`, `numero_parcelas` (getters/setters) — com validações.
  - `confirmar()` — marca pagamento como confirmado.
  - `estornar()` — cancela o pagamento.
- **Validações**: Valor > 0, parcelas entre 1-12, método válido.

---

### Classe `Cupom`

- **Responsabilidade**: representar cupons de desconto.
- **Atributos principais**
  - `_codigo: str` — código único, acessado via `@property`.
  - `_percentual_desconto: float` — desconto em % (0-100), acessado via `@property`.
  - `_valor_minimo_compra: float` — valor mínimo para aplicar, acessado via `@property`.
  - `_ativo: bool` — cupom ativo, acessado via `@property`.
  - `_data_criacao: datetime` — data de criação.
- **Métodos principais**
  - `codigo`, `percentual_desconto`, `valor_minimo_compra`, `ativo` (getters/setters).
  - `validar(valor_compra: float) -> bool` — verifica se cupom é aplicável.
  - `calcular_desconto(subtotal: float) -> float` — retorna valor de desconto.
  - `aplicar_desconto(subtotal: float) -> float` — retorna subtotal com desconto.
- **Validações**: Percentual entre 0-100, valor mínimo ≥ 0.

---

### Classe `Frete`

- **Responsabilidade**: representar cálculo de frete.
- **Atributos principais**
  - `cep_origem: str` — CEP de origem.
  - `cep_destino: str` — CEP de destino.
  - `peso_kg: float` — peso total em kg.
  - `dimensoes: dict` — altura, largura, profundidade em cm.
  - `transportadora: str` — nome da transportadora.
- **Métodos principais**
  - `calcular_frete() -> float` — calcula valor do frete.
  - `consultar_rastreamento(codigo: str) -> str` — retorna status de rastreamento.
- **Relacionamentos**: Utilizado por `Pedido` para composição do valor final.


# 4. Estruturação Modular do Projeto (Atual):

| 📁 **Arquivo / Camada** | 🎯 **Função** | 📌 **Contém** | 📌 **Status** |
|-------------------------|--------------|----------------|----------------|
| `README.md` | Documentação | introdução, UML, estrutura | ✅ |
| `requirements.txt` | Dependências | FastAPI, Uvicorn, Pydantic, SQLite3, etc. | ✅ |
| `.gitignore` | Git config | exclusões de arquivos temporários | ✅ |
| `core/` | Classes de negócio | Produto, Cliente, Pedido, Pagamento, etc. | ✅ |
| `api/` | API REST (FastAPI) | Routers e endpoints | ✅ |
| `db/` | Persistência | SQLite + funções CRUD | ✅ |
| `services/` | Lógica de Frete, relatórios e validações | Cálculos, validações, fluxos | ✅ |

**Representação visual**

```
Projeto_Loja_Virtual/
│
├─ README.md                          # Documentação do projeto
├─ requirements.txt                   # Dependências Python
├─ .gitignore                         # Configuração Git
│
├─ core/                              # 📦 Módulo de classes de negócio
│  ├─ __init__.py
│  ├─ cliente.py                      # Classe Cliente
│  ├─ endereco.py                     # Classe Endereco
│  ├─ produto.py                      # Classe base Produto (Abstract)
│  ├─ produto_fisico.py               # Subclasse ProdutoFisico
│  ├─ produto_digital.py              # Subclasse ProdutoDigital
│  ├─ carrinho.py                     # Classe Carrinho
│  ├─ item_carrinho.py                # Classe ItemCarrinho
│  ├─ pedido.py                       # Classe Pedido
│  ├─ item_pedido.py                  # Classe ItemPedido
│  ├─ pagamento.py                    # Classe Pagamento
│  ├─ cupom.py                        # Classe Cupom
│  ├─ frete.py                        # Classe Frete
│  └─ ...outros módulos               # (expandível)
│
├─ api/                               # 🌐 API REST (FastAPI)
│  ├─ __init__.py
│  ├─ main.py                         # Aplicação FastAPI principal
│  ├─ cliente_route.py                # Endpoints de clientes
│  ├─ produto_route.py                # Endpoints de produtos
│  ├─ carrinho_route.py               # Endpoints de carrinho
│  ├─ pedido_route.py                 # Endpoints de pedidos
│  ├─ cupom_route.py                  # Endpoints de cupons
│  ├─ pagamento_route.py              # Endpoints de pagamentos
│  ├─ frete_route.py                  # Endpoints de frete
│  ├─ estoque_route.py                # Endpoints de estoque
│  ├─ relatorios_route.py             # Endpoints de relatórios
│  └─ admin_route.py                  # Endpoints administrativos
│
├─ db/                                # 💾 Persistência de dados
│  ├─ __init__.py
│  ├─ database.py                     # Funções CRUD e conexão SQLite
│  └─ database.db                     # Arquivo SQLite (gerado)
│
├─ services/                          # 🔧 Serviços de negócio
│  ├─ __init__.py
│  └─ ...serviços específicos          # (expandível)
│
└─ utils/                             # 📦 Funções utilitárias
```

# 5. Checklist do Projeto — Sistema de Loja Virtual com API REST

**Semana 1**
* [X] **UML Textual:** Classes, atributos, métodos e relacionamentos.
* [X] **README Inicial:** Descrição do projeto e estrutura planejada.
* [X] **Classes Iniciais:** Arquivos com classes vazias e docstrings.

**Semana 2**
* [X] **Classes Base:** Produto, Cliente, Endereco, Carrinho, ItemCarrinho.
* [X] **Encapsulamento:** Validações com `@property` e regras de negócio básicas.
* [X] **Métodos Especiais:** `__len__`, `__eq__`, `__repr__`.


**Semana 3**
* [X] **Herança:** ProdutoFisico e ProdutoDigital herdam de Produto.
* [X] **Relacionamentos:** Pedido, ItemPedido, Pagamento, Cupom, Frete.
* [X] **Persistência:** SQLite com funções CRUD em `db/database.py`.
* [X] **API REST (FastAPI):** Endpoints para todos os recursos:
  * [X] `cliente_route.py` - CRUD de clientes
  * [X] `produto_route.py` - CRUD de produtos
  * [X] `carrinho_route.py` - Operações de carrinho
  * [X] `pedido_route.py` - Gerenciamento de pedidos
  * [X] `cupom_route.py` - Validação e aplicação de cupons
  * [X] `pagamento_route.py` - Processamento de pagamentos
  * [X] `frete_route.py` - Cálculo e rastreamento de frete
  * [X] `estoque_route.py` - Gerenciamento de estoque
  * [X] `relatorios_route.py` - Relatórios de vendas
  * [X] `admin_route.py` - Funções administrativas

**Semana 4**
* [X] **Testes Automatizados:**
  * [X] `test_api.py` - Testes dos endpoints
  * [X] `test_integracao.py` - Testes de fluxos completos
  * [X] Validações de entrada e regras de negócio
* [X] **Documentação Interativa:** Swagger UI em `/docs` (FastAPI)
* [X] **Git:** `.gitignore` configurado

**Semana 5**
* [X] **SKU em Produtos:** Campo adicionado e salvável no banco
* [X] **Endpoints Administrativos:**
  * [X] `DELETE /admin/limpar/produtos` - Limpar todos os produtos
  * [X] `DELETE /admin/limpar/clientes` - Limpar todos os clientes
  * [X] `DELETE /admin/resetar-banco` - Resetar banco completamente
  * [X] `GET /admin/status` - Status do banco
* [X] **Validações Robustas:**
  * [X] CPF/Email únicos e válidos
  * [X] CEP com 8 dígitos
  * [X] SKU único por produto
  * [X] Limite de itens no carrinho
  * [X] Estoque suficiente

---

# 6. Como Usar a API

## Instalação e Setup

```bash
# 1. Clonar o repositório
git clone <repo-url>
cd Projeto_Loja_Virtual

# 2. Criar ambiente virtual
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar a API
uvicorn api.main:app --reload
```

A API estará disponível em: **http://localhost:8000**

## Acessar Documentação Interativa

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Exemplos de Requisições

### 1. Criar Cliente
```bash
curl -X POST "http://localhost:8000/clientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "123.456.789-10",
    "email": "joao@example.com",
    "endereco": []
  }'
```

### 2. Criar Produto Físico
```bash
curl -X POST "http://localhost:8000/produtos/fisico" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Notebook",
    "descricao": "Notebook de alta performance",
    "preco": 2500.00,
    "peso": 2.5,
    "altura": 30,
    "largura": 20,
    "profundidade": 2,
    "sku": "NOTEBOOK-001"
  }'
```

### 3. Listar Produtos
```bash
curl -X GET "http://localhost:8000/produtos"
```

### 4. Criar Carrinho
```bash
curl -X POST "http://localhost:8000/carrinhos/criar?cliente_cpf=123.456.789-10"
```

### 5. Ver Status do Banco
```bash
curl -X GET "http://localhost:8000/admin/status"
```

### 6. Limpar Produtos
```bash
curl -X DELETE "http://localhost:8000/admin/limpar/produtos"
```

## Testar a API

Você pode testar a API de forma interativa usando o Swagger:

```bash
# 1. Iniciar o servidor
python -m uvicorn api.main:app --reload

# 2. Acessar o Swagger (documentação interativa)
# Abra no navegador: http://localhost:8000/docs
```

A documentação interativa permite fazer requisições diretamente na interface, consultando todos os endpoints disponíveis.

---

# 7. Arquitetura da Aplicação

## Camadas

1. **Core (`core/`)** - Modelos de negócio com validações e regras
2. **API (`api/`)** - Endpoints REST para comunicação externa
3. **Database (`db/`)** - Persistência em SQLite
4. **Services (`services/`)** - Validações de negócio e cálculos
5. **Tests (`tests/`)** - Testes automatizados

## Fluxo de uma Requisição

```
Cliente HTTP
    ↓
FastAPI Route (api/*.py)
    ↓
Classe Core (core/*.py) - Validações de formato
    ↓
Services (services/services_database.py) - Validações de negócio
    ↓
Database (db/database.py) - Persistência
    ↓
Resposta JSON
```

---

# 8. Sistema de Validações

## 🔐 Validações em Três Camadas

### Camada 1: Validações de Domínio (core/)
Validações de formato em properties das classes:
- **CPF:** Formato XXX.XXX.XXX-XX e algoritmo
- **Email:** Formato de email válido
- **Produto:** Preço > 0, peso > 0, dimensões > 0
- **Cupom:** Desconto 0-100%, valor mínimo ≥ 0

### Camada 2: Validações de Banco (services/services_database.py)
Validações de regras de negócio e unicidade:
- **SKU Único:** Garante que cada SKU é único no sistema
- **CPF/Email Único:** Previne duplicação de clientes
- **Limite Carrinho:** Máximo 50 itens por carrinho
- **Estoque Suficiente:** Valida quantidade disponível
- **Cliente Existe:** Verifica existência antes de pedido
- **Cupom Válido:** Verifica código, data e valor mínimo
- **Endereço Válido:** CEP, número, cidade e UF

### Camada 3: Validações de API (api/*.py)
Resposta HTTP com erro 400 e mensagem descritiva

## ✅ Validações Implementadas

| Validação | Função | Local | Status |
|-----------|--------|-------|--------|
| SKU Único | `validar_sku_unico()` | `produto_route.py` | ✅ |
| CPF Único | `validar_cpf_unico()` | `cliente_route.py` | ✅ |
| Email Único | `validar_email_unico()` | `cliente_route.py` | ✅ |
| Limite Carrinho | `validar_limite_itens_carrinho()` | `carrinho_route.py` | ✅ |
| Estoque Suficiente | `validar_estoque_suficiente()` | `carrinho_route.py` | ✅ |
| Cliente Existe | `validar_cliente_existe()` | `pedido_route.py` | ✅ |
| Endereço Válido | `validar_pedido_endereco_valido()` | `pedido_route.py` | ✅ |
| Cupom Válido | `validar_cupom_existe/ativo/valor_minimo()` | `pedido_route.py` | ✅ |

## 🧪 Testes de Validação

Cobertura com 20+ testes em `tests/test_services_database.py`:

```bash
# Executar testes de validação
pytest tests/test_services_database.py -v
```

**Testes Incluídos:**
- TestValidarSkuUnico (2 testes)
- TestValidarCpfUnico (2 testes)
- TestValidarEmailUnico (2 testes)
- TestValidarLimiteItensCarrinho (2 testes)
- TestValidarEstoqueSuficiente (2 testes)
- TestValidarEnderecoValido (3 testes)
- TestValidarCupomExiste/Ativo/ValorMinimo (5 testes)

## 📝 Exemplos de Testes via API

### Testar SKU Duplicado
```bash
# Criar primeiro produto com SKU
curl -X POST http://localhost:8000/produtos/fisico \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Produto", "preco": 100, "peso": 1,
    "altura": 10, "largura": 10, "profundidade": 10, "sku": "SKU-001"
  }'

# Tentar criar com SKU duplicado (retorna 400)
curl -X POST http://localhost:8000/produtos/fisico \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Outro", "preco": 200, "peso": 1,
    "altura": 10, "largura": 10, "profundidade": 10, "sku": "SKU-001"
  }'
# {"detail": "SKU SKU-001 já existe no banco de dados"}
```

### Testar Limite de Carrinho
```bash
# Tentar adicionar 51 itens (retorna 400)
curl -X POST http://localhost:8000/carrinhos/12345678901/itens \
  -H "Content-Type: application/json" \
  -d '{"produto_sku": "SKU-001", "quantidade": 51}'
# {"detail": "Limite máximo de 50 itens no carrinho excedido"}
```

---

# 9. Aprendizados e Desenvolvimento

## 📚 Principais Conceitos Aplicados

- **Programação Orientada a Objetos:** Classes, herança, encapsulamento, validações com properties
- **Design Patterns:** Separação em camadas (Domain, Database, API), Services pattern
- **Persistência:** SQLite com operações CRUD e context managers
- **API REST:** FastAPI com validação automática (Pydantic), documentação Swagger

## 🚀 Evolução do Projeto

### Fases de Desenvolvimento

1. **Fase 1:** Conceitos básicos de POO
2. **Fase 2:** Estrutura completa com herança e relacionamentos
3. **Fase 3:** Integração com SQLite e operações CRUD
4. **Fase 4:** Criação da API REST com FastAPI
5. **Fase 5:** Validações de negócio em múltiplas camadas
   - SKU em produtos
   - Módulo `services_database.py` com 15+ validações
   - Integração em todos endpoints
   - Limpeza de dados de entrada (CPF, CEP, etc.)

### Decisão Arquitetural

**Linha de Desenvolvimento:** Classe → Banco de Dados → API Routes

Benefícios:
- Regras de negócio claras e encapsuladas
- Persistência confiável e testável
- Endpoints simples e focados
- Validações em múltiplas camadas

## 🔍 Desafios Enfrentados

| Desafio | Solução |
|---------|---------|
| Integração inicial complexa | Arquitetura clara: Classe → DB → API |
| Validações espalhadas | Centralizar em `services_database.py` |
| Mensagens de erro genéricas | Mensagens descritivas com HTTP 400 |
| Formatação de dados (CPF, CEP) | Funções de limpeza em `services/utils.py` |

---

