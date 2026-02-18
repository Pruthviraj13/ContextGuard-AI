from fastapi import APIRouter, HTTPException,Depends
from app.schemas.request import QueryRequest
from app.schemas.response import QueryResponse
from app.core.security import get_current_user

from app.services.classifier import QueryClassifier, QueryType
from app.services.retriever import Retriever
from app.services.generator import LLMGenerator
from app.services.evaluator import AnswerEvaluator

evaluator = AnswerEvaluator()

generator = LLMGenerator()
classifier = QueryClassifier()
router = APIRouter()
@router.post("/")
async def query_rag(
    request: QueryRequest,
    user: dict = Depends(get_current_user)
):
    query_type = classifier.classify(request.question)

    if query_type == QueryType.FORBIDDEN:
        raise HTTPException(status_code=403, detail="Forbidden query")

    if query_type == QueryType.NO_RAG:
        return {
            "answer": "This question does not require document lookup.",
            "confidence": 0.9,
            "sources": []
        }

    if query_type == QueryType.UNSUPPORTED:
        raise HTTPException(status_code=400, detail="Unsupported query")

    # Only RAG_REQUIRED reaches here
    retriever = Retriever()

    if query_type == QueryType.RAG_REQUIRED:
        chunks = retriever.retrieve(request.question)
        texts = [c["text"] for c in chunks]
        print(f"Retrieved {len(texts)} chunks")
        print(f"Chunks preview: {texts[:1]}")
        

        answer = await generator.generate(
            question=request.question,
            context_chunks=texts
        )
        confidence = evaluator.evaluate(answer, texts)
        print(f"Generated answer: {answer}")
        print(f"Confidence score: {confidence}")
        if confidence < 0.4:
            return {
                "answer": "I’m not confident enough to answer based on the available documents.",
                "confidence": confidence,
                "sources": []
            }
        return {
            "answer": answer,
            "confidence": 0.8,
            "sources": [c["source"] for c in chunks]
        }
\

