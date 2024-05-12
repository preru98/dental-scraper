from fastapi import FastAPI
from dental.routers.dental import router as dental_router
from dental.routers.health import router as health_router

app = FastAPI()

app.include_router(health_router)
app.include_router(dental_router)
