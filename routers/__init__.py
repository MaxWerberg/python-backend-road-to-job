from fastapi import APIRouter

from routers.address_router import address_router
from routers.admin_router import admin_router
from routers.cart_router import cart_router
from routers.order_router import order_router
from routers.product_router import admin_product_router, product_router
from routers.user_router import user_router

main_router = APIRouter()

main_router.include_router(user_router)
main_router.include_router(address_router)
main_router.include_router(product_router)
main_router.include_router(admin_product_router)
main_router.include_router(admin_router)
main_router.include_router(cart_router)
main_router.include_router(order_router)
