from decimal import Decimal

from fastapi import Request

from .base_form import BaseForm
from py_schemas.product import CreateProduct


class ProductForm(BaseForm):
    name: str | None
    description: str | None
    price: Decimal | None

    async def load_form_data(self):
        form_data = await self.request.form()

        self.name = form_data.get("product_name")
        self.description = form_data.get("product_description")
        self.price = form_data.get("product_price")

    def form_to_schema(self):
        product_data = CreateProduct(
            name=self.name, description=self.description, price=self.price
        )

        return product_data
