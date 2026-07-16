from fastapi import APIRouter, Depends, HTTPException, status

from dependencies.service_dependencies import get_product_service as serv_dep
from schemas.product_schema import ProductRegisterSchema, ProductResponseSchema
from services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Product"])


@router.post("/register", response_model=ProductResponseSchema)
def register_product(
    product_data: ProductRegisterSchema,
    product_service: ProductService = Depends(serv_dep),
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
