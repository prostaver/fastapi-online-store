from fastapi import Request

from .base_form import BaseForm


class CartForm(BaseForm):
    product_id: int | None
    quantity: int | None

    async def load_form_data(self) -> None:
        form_data = await self.request.form()
        self.product_id = form_data.get("cart_product_id")
        self.quantity = form_data.get("cart_product_quantity")
