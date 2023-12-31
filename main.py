from fastapi import FastAPI, HTTPException

# Documentation
from documentations.description import api_description
from documentations.tags import tags_metadata

#Routers
import routers.router_musics
import routers.router_users
import routers.router_auth
import routers.router_stripe
# Initialisation de l'API
app = FastAPI(
    title="Music Platform",
    description=api_description,
    openapi_tags= tags_metadata,
    docs_url='/'
)

# Router dédié aux Students
app.include_router(routers.router_musics.router)
app.include_router(routers.router_users.router)
app.include_router(routers.router_auth.router)
app.include_router(routers.router_stripe.router)
