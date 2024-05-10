from fastapi import FastAPI
from routers.router_todos import router as todos_router


app = FastAPI(
    title="TodoList API",
    docs_url='/'
)

app.include_router(todos_router)
