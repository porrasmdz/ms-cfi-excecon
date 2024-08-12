from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.utils import filters_to_sqlalchemy
from typing import List, Any
from app.dependencies import get_table_query_body
from app.schemas import TableQueryBody, PaginatedResource
from . import service
from ..database import get_session
from fastapi import APIRouter


router = APIRouter(tags=["ETL Module"])

