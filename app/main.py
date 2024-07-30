from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.inventory.router import router as inventory_router
from app.companies.router import router as companies_router
from app.cyclic_count.router import router as cyclic_count_router
from starlette.concurrency import iterate_in_threadpool
from .database import init_db
import json
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
# Might add middleware to append total_results and skip, limit in ContentRange on headers
# Middleware appending processing time to response example
@app.middleware("http")
async def append_content_range_header(request: Request, call_next):
    response = await call_next(request)
    response_body = [chunk async for chunk in response.body_iterator]
    try:
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        response_json = json.loads(response_body[0].decode())
        total_results = response_json['totalResults']
        skip = response_json['skip']
        limit = response_json['limit']
        response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
        response.headers["Content-Range"] = f"resources {skip}-{limit}/{total_results}"
        print("appended content-range", response.method)
    except: pass
    return response

init_db()
app.include_router(inventory_router)
app.include_router(companies_router)
app.include_router(cyclic_count_router)


