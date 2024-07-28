from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.inventory.router import router as inventory_router
from app.companies.router import router as companies_router
from app.cyclic_count.router import router as cyclic_count_router
from .database import init_db

app = FastAPI()

init_db()
app.include_router(inventory_router)
app.include_router(companies_router)
app.include_router(cyclic_count_router)


