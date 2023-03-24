from fastapi import Request


class BaseForm:
    request: Request

    def __init__(self, request: Request):
        self.request = request

    async def load_form_data(self):
        pass

    def form_to_schema(self):
        pass
