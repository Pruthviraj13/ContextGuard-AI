from enum import Enum

class QueryType(str, Enum):
    RAG_REQUIRED = "rag_required"
    NO_RAG = "no_rag"
    FORBIDDEN = "forbidden"
    UNSUPPORTED = "unsupported"

    
class QueryClassifier:

    FORBIDDEN_KEYWORDS = [
        "ignore previous",
        "system prompt",
        "jailbreak",
        "bypass",
    ]

    RAG_KEYWORDS = [
        "policy",
        "document",
        "agreement",
        "contract",
        "refund",
        "terms",
    ]

    def classify(self, question: str) -> QueryType:
        q = question.lower()

        # 1️⃣ Forbidden
        for word in self.FORBIDDEN_KEYWORDS:
            if word in q:
                return QueryType.FORBIDDEN

        # 2️⃣ Needs RAG
        for word in self.RAG_KEYWORDS:
            if word in q:
                return QueryType.RAG_REQUIRED

        # 3️⃣ Too short / junk
        if len(q.split()) < 3:
            return QueryType.NO_RAG

        # 4️⃣ Default
        return QueryType.UNSUPPORTED

