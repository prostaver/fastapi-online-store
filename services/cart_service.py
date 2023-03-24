from sqlalchemy.orm import Session

from models.cart import Cart
from models.user import User


def add_to_cart(
    db: Session, user: User, product_id: int, quantity: int
) -> None:
    cart = Cart(user_id=user.id, product_id=product_id, quantity=quantity)

    db.add(cart)
    db.commit()


def remove_from_cart(db: Session, user: User, cart_obj_id: int) -> None:
    to_be_deleted = db.query(Cart).filter(Cart.id == cart_obj_id).first()

    db.delete(to_be_deleted)
    db.commmit()


def get_cart_item(db: Session, user: User, cart_item_id: int) -> Cart:
    return db.query(Cart).filter(Cart.id == cart_item_id).first()
