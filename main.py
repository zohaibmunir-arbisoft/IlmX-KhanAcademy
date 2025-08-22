import time

from app.auth.router import auth_router
from app.llm_services.router import llm_services_router

from fastapi import FastAPI, Request
from loguru import logger

fastapi_app = FastAPI(title="IlmX-Khan Academy", version="0.1.0")
logger.add("app.log", rotation="500 MB", compression="zip", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")

@fastapi_app.get("/", tags=["Homepage"])
async def homepage() -> dict:
    """
    Check Web server is running
    """
    return {"status": "Server is running 🚀"}


@fastapi_app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Middleware function to add a process time header to the HTTP response.

    Parameters:
        request (Request): The incoming HTTP request.
        call_next (function): The next middleware or endpoint handler in the chain.

    Returns:
        Response: The HTTP response object with the added process time header.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 2))
    return response


fastapi_app.include_router(auth_router)
fastapi_app.include_router(llm_services_router)
