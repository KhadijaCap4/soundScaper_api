from fastapi import FastAPI
from routers.router_todos import router as todos_router
from documentations.description import api_description
from documentations.tags import tags_metadata

app = FastAPI(
    title="TodoList API",
    description=api_description,
    openapi_tags=tags_metadata,
    docs_url='/'
)

app.include_router(todos_router)
