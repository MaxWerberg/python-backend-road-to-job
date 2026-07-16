from fastapi import FastAPI

from routers.product_router import router as product_router
from routers.user_router import router as user_router

app = FastAPI()
app.include_router(user_router)
app.include_router(product_router)


@app.get("/")
def root():
    return {"message": "fastApi работает"}
