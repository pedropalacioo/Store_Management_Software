from fastapi import FastAPI
from api.cliente_route import router as cliente_router
from api.produto_route import router as produto_router
from api.carrinho_route import router as carrinho_router
from api.pedido_route import router as pedido_router
from api.cupom_route import router as cupom_router
from api.pagamento_route import router as pagamento_router
from api.frete_route import router as frete_router
from api.estoque_route import router as estoque_router
from api.relatorios_route import router as relatorios_router
from api.admin_route import router as admin_router

app = FastAPI(title = "API da loja Virtual", version = "1.0")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API da Loja Virtual!"}

# Registrar todos os routers
app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(carrinho_router)
app.include_router(pedido_router)
app.include_router(cupom_router)
app.include_router(pagamento_router)
app.include_router(frete_router)
app.include_router(estoque_router)
app.include_router(relatorios_router)
app.include_router(admin_router)