from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from config.database import get_db_connection
from forms.product_form import ProductForm
from py_schemas import product as product_schema
from routes.endpoints.login import oauth2_scheme
from services import product_service
from views import templates

router = APIRouter(prefix="/products", tags=["products"])


@router.get(
    "/",
    response_model=list[product_schema.Product],
    status_code=status.HTTP_200_OK,
)
async def get_products(db: Session = Depends(get_db_connection)):
    return product_service.get_products(db)


@router.get(
    "/{product_id}",
    response_model=product_schema.Product,
    status_code=status.HTTP_200_OK,
)
async def get_product(
    product_id: int, db: Session = Depends(get_db_connection)
):
    return product_service.get_product(db, product_id)


@router.post(
    "/",
    response_model=product_schema.Product,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_input: product_schema.CreateProduct,
    db: Session = Depends(get_db_connection),
):
    return product_service.create_product(db, product_input)


@router.post(
    "/{product_id}",
    response_model=product_schema.Product,
    status_code=status.HTTP_200_OK,
)
async def update_product(
    product_id: int,
    product_input: product_schema.CreateProduct,
    db: Session = Depends(get_db_connection),
):
    return product_service.update_product(db, product_input, product_id)


@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db_connection),
    token: str = Depends(oauth2_scheme),
):
    return product_service.delete_product(db, product_id)


@router.get("/form/", response_class=HTMLResponse)
async def product_form(request: Request):
    return templates.TemplateResponse(
        "forms/product.html", {"request": request}
    )


@router.post("/form/", response_class=HTMLResponse)
async def post_product_form(
    request: Request, db: Session = Depends(get_db_connection)
):
    form = ProductForm(request)

    try:
        # response = RedirectResponse(
        #     request.url_for("dashboard"), status.HTTP_303_SEE_OTHER
        # )

        await form.load_form_data()

        product_input = form.form_to_schema()
        await create_product(product_input=product_input, db=db)

        # return response
    except HTTPException as e:
        form.__dict__.update(errors=e.detail)
        return templates.TemplateResponse("forms/product.html", form.__dict__)


@router.get("/list/", response_class=HTMLResponse)
async def page_product_list(
    request: Request, db: Session = Depends(get_db_connection)
):
    products = product_service.get_products(db=db)

    data = {"request": request, "products": products}

    return templates.TemplateResponse("pages/products.html", data)


@router.get("/{product_id}/details/", response_class=HTMLResponse)
async def product_details(
    request: Request, product_id: int, db: Session = Depends(get_db_connection)
):
    product = await get_product(product_id=product_id, db=db)

    data = {"request": request, "product": product}

    return templates.TemplateResponse("pages/product_detail.html", data)
