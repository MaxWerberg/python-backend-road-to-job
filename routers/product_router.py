from fastapi import APIRouter, Depends, Response, status

from dependencies.auth_dependencies import require_admin
from dependencies.type_dependencies import ProductServiceDep
from schemas.product_schema import (
    ProductChangeCostSchema,
    ProductDeleteSchema,
    ProductReceiveOrShipSchema,
    ProductRegisterSchema,
    ProductResponseSchema,
    ProductSearchSchema,
)

product_router = APIRouter(prefix="/products", tags=["Product"])
admin_product_router = APIRouter(
    prefix="/products", tags=["Product"], dependencies=[Depends(require_admin)]
)


@product_router.get("/product", response_model=ProductResponseSchema)
def get_product_info(
    product_search: ProductSearchSchema,
    product_service: ProductServiceDep,
):
    return product_service.find_product(
        product_id=product_search.id, product_sku=product_search.sku
    )


@admin_product_router.post("/register", response_model=ProductResponseSchema)
def register_product(
    product_data: ProductRegisterSchema,
    product_service: ProductServiceDep,
):

    return product_service.create_product(
        sku=product_data.sku,
        product_name=product_data.product_name,
        product_cost=product_data.product_cost,
        stock_quantity=product_data.stock_quantity,
    )


@admin_product_router.patch("/product/cost", response_model=ProductResponseSchema)
def change_product_cost(
    product_search: ProductChangeCostSchema,
    product_service: ProductServiceDep,
):
    return product_service.change_cost(
        product_id=product_search.id,
        product_sku=product_search.sku,
        new_cost=product_search.new_cost,
    )


@admin_product_router.patch(
    "/product/receive_stock", response_model=ProductResponseSchema
)
def receive_stock_product(
    product_search: ProductReceiveOrShipSchema,
    product_service: ProductServiceDep,
):
    return product_service.receive_stock(
        product_id=product_search.id,
        product_sku=product_search.sku,
        quantity=product_search.quantity,
    )


@admin_product_router.patch("/product/ship_stock", response_model=ProductResponseSchema)
def ship_stock_product(
    product_search: ProductReceiveOrShipSchema,
    product_service: ProductServiceDep,
):
    return product_service.ship_stock(
        product_id=product_search.id,
        product_sku=product_search.sku,
        quantity=product_search.quantity,
    )


@admin_product_router.delete("/product")
def delete_product(
    product: ProductDeleteSchema,
    product_service: ProductServiceDep,
):

    product_service.delete_product(product_id=product.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
