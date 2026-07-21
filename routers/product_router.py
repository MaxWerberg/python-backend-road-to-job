from fastapi import APIRouter, Depends, HTTPException, Response, status

from dependencies.service_dependencies import get_product_service as serv_prod_dep
from schemas.product_schema import (
    ProductChangeCostSchema,
    ProductDeleteSchema,
    ProductReceiveOrShipSchema,
    ProductRegisterSchema,
    ProductResponseSchema,
    ProductSearchSchema,
)
from services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Product"])


@router.get("/product", response_model=ProductResponseSchema)
def get_product_info(
    product_search: ProductSearchSchema,
    product_service: ProductService = Depends(serv_prod_dep),
):
    try:
        if product_search.id is not None:
            return product_service.get_product_by_id(product_id=product_search.id)

        if product_search.sku is not None:
            return product_service.get_product_by_sku(product_sku=product_search.sku)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.post("/register", response_model=ProductResponseSchema)
def register_product(
    product_data: ProductRegisterSchema,
    product_service: ProductService = Depends(serv_prod_dep),
):

    try:
        return product_service.create_product(
            sku=product_data.sku,
            product_name=product_data.product_name,
            product_cost=product_data.product_cost,
            stock_quantity=product_data.stock_quantity,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.patch("/product/cost", response_model=ProductResponseSchema)
def change_product_cost(
    product_search: ProductChangeCostSchema,
    product_service: ProductService = Depends(serv_prod_dep),
):

    try:
        product_id = product_search.id

        if product_id is None:
            product = product_service.get_product_by_sku(product_sku=product_search.sku)
            product_id = product.id

        return product_service.change_cost(
            product_id=product_id,
            new_cost=product_search.new_cost,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch("/product/receive_stock", response_model=ProductResponseSchema)
def receive_stock_product(
    product_search: ProductReceiveOrShipSchema,
    product_service: ProductService = Depends(serv_prod_dep),
):

    try:
        product_id = product_search.id

        if product_id is None:
            product = product_service.get_product_by_sku(product_sku=product_search.sku)
            product_id = product.id

        return product_service.receive_stock(
            product_id=product_id, quantity=product_search.quantity
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.patch("/product/ship_stock", response_model=ProductResponseSchema)
def ship_stock_product(
    product_search: ProductReceiveOrShipSchema,
    product_service: ProductService = Depends(serv_prod_dep),
):

    try:
        product_id = product_search.id

        if product_id is None:
            product = product_service.get_product_by_sku(product_sku=product_search.sku)
            product_id = product.id

        return product_service.ship_stock(
            product_id=product_id, quantity=product_search.quantity
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error))


@router.delete("/product")
def delete_product(
    product_search: ProductDeleteSchema,
    product_service: ProductService = Depends(serv_prod_dep),
):

    try:
        product_id = product_search.id
        if product_id is None:
            product = product_service.get_product_by_sku(product_sku=product_search.sku)
            product_id = product.id

        product_service.delete_product(product_id=product_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        )
