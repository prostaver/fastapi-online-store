from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.database import get_db_connection
from forms.login_form import LoginForm
from handlers.auth_bearer_with_cookie_handler import (
    OAuth2PasswordBearerWithCookie,
)
from services import login_service
from views import templates

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/login/token")


@router.post("/login/token", tags=["login"])
def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db_connection),
):
    return login_service.create_auth_token(
        db, form_data.username, form_data.password, response
    )


@router.get("/login/", tags=["login"], response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("forms/login.html", {"request": request})


@router.post("/login/", tags=["login"], response_class=HTMLResponse)
async def post_login_form(
    request: Request, db: Session = Depends(get_db_connection)
):
    form = LoginForm(request)

    try:
        response = RedirectResponse(
            request.url_for("dashboard"), status.HTTP_303_SEE_OTHER
        )
        await form.load_form_data()
        login(response=response, form_data=form, db=db)
        return response
    except HTTPException as e:
        form.__dict__.update(errors=e.detail)
        return templates.TemplateResponse("forms/login.html", form.__dict__)
