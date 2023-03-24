from fastapi import APIRouter

from .endpoints import cart, dashboard, login, order, product, user

router = APIRouter()

router.include_router(login.router)
router.include_router(dashboard.router)
router.include_router(product.router)
router.include_router(cart.router)
router.include_router(order.router)
router.include_router(user.router)
