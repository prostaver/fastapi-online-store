from fastapi import Request


class LoginForm:
    request: Request
    username: str | None
    password: str | None

    def __init__(self, request: Request):
        self.request = request

    async def load_form_data(self):
        form_data = await self.request.form()

        self.username = form_data.get("username")
        self.password = form_data.get("password")
