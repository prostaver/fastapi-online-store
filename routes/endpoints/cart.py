from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from config.database import get_db_connection
from forms.cart_form import CartForm
from models.user import User
from routes.endpoints.user import get_current_user
from services import cart_service


router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/add/", response_class=HTMLResponse)
async def add_to_cart(
    request: Request,
    user_or_response: User | RedirectResponse = Depends(get_current_user),
    db: Session = Depends(get_db_connection),
):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    form = CartForm(request)
    await form.load_form_data()

    cart_service.add_to_cart(
        db=db,
        user=user_or_response,
        product_id=form.product_id,
        quantity=form.quantity,
    )


async def get_cart(
    request: Request,
    user_or_response: User | RedirectResponse = Depends(get_current_user),
    db: Session = Depends(get_db_connection),
):
    if isinstance(user_or_response, RedirectResponse):
        return user_or_response

    ...
