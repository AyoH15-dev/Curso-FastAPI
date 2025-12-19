from pydantic import BaseModel

class User(BaseModel):
    id: str | None = None # | None: Permite que el id sea opcional
    username: str
    email: str