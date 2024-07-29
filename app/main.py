from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.inventory.router import router as inventory_router
from app.companies.router import router as companies_router
from app.cyclic_count.router import router as cyclic_count_router
from .database import init_db

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Might add middleware to append total_results and skip, limit in ContentRange on headers
# Middleware appending processing time to response example
# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     response.headers["X-Process-Time"] = str(process_time)
#     return response

init_db()
app.include_router(inventory_router)
app.include_router(companies_router)
app.include_router(cyclic_count_router)


