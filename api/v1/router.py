from fastapi import APIRouter
from app.api.v1.endpoints import rag, health, ingest,auth

router = APIRouter()

router.include_router(rag.router, prefix="/query", tags=["RAG"])
router.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
router.include_router(health.router, prefix="/health", tags=["Health"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
