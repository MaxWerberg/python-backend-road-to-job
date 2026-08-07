from fastapi import FastAPI

from errors import register_error_handlers
from routers.admin_router import admin_router
from routers.cart_router import cart_router
from routers.product_router import admin_product_router, product_router
from routers.user_router import user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(admin_product_router)
app.include_router(admin_router)
app.include_router(cart_router)


@app.get("/")
def root():
    return {"message": "fastApi работает"}


register_error_handlers(app)
