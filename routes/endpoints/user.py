from typing import List

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .login import oauth2_scheme
from config.database import get_db_connection
from forms.user_form import UserForm
from py_schemas import user as user_schema
from services import login_service, user_service
from views import templates

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/", response_model=List[user_schema.User], status_code=status.HTTP_200_OK
)
async def get_users(db: Session = Depends(get_db_connection)):
    users = user_service.get_users(db)
    return users


@router.get(
    "/{user_id}",
    response_model=user_schema.User,
    status_code=status.HTTP_200_OK,
)
async def get_user(user_id: int, db: Session = Depends(get_db_connection)):
    return user_service.get_user(db, user_id)


@router.post(
    "/", response_model=user_schema.User, status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_input: user_schema.CreateUser,
    db: Session = Depends(get_db_connection),
):
    return user_service.create_user(db, user_input)


@router.post(
    "/{user_id}",
    response_model=user_schema.User,
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_user(
    user_id: int,
    user_input: user_schema.CreateUser,
    db: Session = Depends(get_db_connection),
):
    return user_service.update_user(db, user_input, user_id)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: Session = Depends(get_db_connection)):
    return user_service.delete_user(db, user_id)


@router.get(
    "/current/",
    response_model=user_schema.User,
    status_code=status.HTTP_200_OK,
)
async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_connection),
):
    if token is not None:
        payload = login_service.decode_token(token)

        if payload is not None:
            return user_service.get_user_by_username(
                db, payload.get("username")
            )

    return RedirectResponse(
        request.url_for("login", status.HTTP_303_SEE_OTHER)
    )


@router.get("/form/admin_user/", response_class=HTMLResponse)
async def get_user_form(request: Request):
    data = {"request": request}
    return templates.TemplateResponse("forms/user.html", data)


@router.post("/form/admin_user/")
async def post_user_form(
    request: Request, db: Session = Depends(get_db_connection)
):
    user_form = UserForm(request)
    await user_form.load_form_data()
    user_data = user_form.form_to_schema()
    await create_user(user_data, db)
