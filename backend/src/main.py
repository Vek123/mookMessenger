import uvicorn

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from users.database import User
from users.auth import auth_backend
from users.manager import get_user_manager
from users.schemas import UserRead, UserCreate


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(
    title="Messenger"
)


@app.get("/roles")
def get_roles():
    return "Hello world"


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
