from fastapi import FastAPI
from dental.routers.dental import dental_router
from dental.routers.health import health_router

app = FastAPI()

app.include_router(health_router)
app.include_router(dental_router)
