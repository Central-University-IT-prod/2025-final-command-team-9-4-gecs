import os
import importlib
from fastapi import FastAPI
from src.database import init
from contextlib import asynccontextmanager
import json

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init()
    yield

app = FastAPI(
    title="4GECS",
    description="Сервис по генерации рандомных аватаров",
    version="0.0.1",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api"
)

def custom_openapi():
    with open("openapi.json", "r") as openapi:
        return json.load(openapi)

app.openapi = custom_openapi

routers_dir = os.path.join(os.path.dirname(__file__), "routers")

for filename in os.listdir(routers_dir):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = filename[:-3]
        module_path = os.path.join(routers_dir, filename)

        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, "router"):
            app.include_router(module.router)