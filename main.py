from fastapi import FastAPI
from app.api.v1.router import router as v1_router
from app.core.rate_limit_middleware import RateLimitMiddleware

app = FastAPI(
    title="Production RAG Backend",
    version="1.0.0"
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)
from app.core.request_context import RequestContextMiddleware

app.add_middleware(RequestContextMiddleware)


app.include_router(v1_router, prefix="/api/v1")

