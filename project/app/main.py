import logging
import os
from fastapi import FastAPI
from project.app.db import init_db
from tortoise.contrib.fastapi import register_tortoise
from app.api import ping

log = logging.getLogger("uvicorn")

def create_application() -> FastAPI:
    application = FastAPI()
    register_tortoise(
    application,
    db_url= os.environ.get("DATABASE_URL"),
    modules={"models" : ["app.models.tortoise"]},
    generate_schemas=False,
    add_exception_handlers=True
)

    application.include_router(ping.router)
    
    return application

app = create_application()

@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)
    
@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")