from fastapi import FastAPI
from dental.api import endpoints

app = FastAPI()

app.include_router(endpoints.router)