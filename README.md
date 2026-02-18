# ContextGuard AI

ContextGuard AI is a production-grade Retrieval-Augmented Generation
(RAG) backend built with FastAPI.\
It delivers grounded, reliable AI responses using selective retrieval,
strict validation, and production-focused backend design.

------------------------------------------------------------------------

## 🚀 Key Features

-   🔐 JWT-based Authentication
-   🧠 Intelligent Query Classification (RAG vs Non-RAG routing)
-   📚 FAISS Vector Index for semantic search
-   🛡 Confidence-based Answer Validation (anti-hallucination guardrail)
-   🔁 Retry & Fallback Strategy for LLM failures
-   📊 Structured Logging & Observability (latency, request IDs)
-   🗑 Soft Delete & Document Lifecycle Management
-   ⚡ Async FastAPI backend (ASGI-based)
-   🧩 Streamlit lightweight testing UI

------------------------------------------------------------------------

## 🏗 Architecture Overview

User → Streamlit UI → FastAPI Backend → Classifier → (RAG or Direct LLM)
→ FAISS Retrieval → LLM Generation → Validation Layer → Response

------------------------------------------------------------------------

## 📦 Project Structure

app/ │ ├── api/ │ └── v1/ │ ├── endpoints/ │ │ ├── auth.py │ │ ├──
rag.py │ │ ├── ingest.py │ │ └── health.py │ └── router.py │ ├──
services/ │ ├── classifier.py │ ├── generator.py │ ├── evaluator.py │
└── retriever.py │ ├── core/ │ ├── logging.py │ ├──
rate_limit_middleware.py │ └── request_context.py │ └── main.py

------------------------------------------------------------------------

## 🔍 How It Works

1.  User sends a question.
2.  Query classifier determines if RAG is required.
3.  If required:
    -   Relevant document chunks are retrieved from FAISS.
    -   LLM generates answer using retrieved context only.
    -   Evaluator validates response and assigns confidence.
4.  If confidence is low → Safe fallback message returned.
5.  All requests logged with latency and request IDs.

------------------------------------------------------------------------

## 🧠 Why This Project Matters

-   Prevents hallucinations instead of hiding them.
-   Uses selective retrieval to reduce cost and latency.
-   Handles LLM failures gracefully.
-   Designed with production reliability in mind.
-   Demonstrates backend + GenAI integration depth.

------------------------------------------------------------------------

## 🛠 How to Run the Application

### 1️⃣ Clone the Repository

git clone `<your-repo-url>`{=html} cd contextguard-ai

------------------------------------------------------------------------

### 2️⃣ Create Virtual Environment

python -m venv venv

Activate:

Windows: venv`\Scripts`{=tex}`\activate`{=tex}

Mac/Linux: source venv/bin/activate

------------------------------------------------------------------------

### 3️⃣ Install Dependencies

pip install -r requirements.txt

------------------------------------------------------------------------

### 4️⃣ Set Environment Variables

Windows (PowerShell): setx GROQ_API_KEY "your_groq_api_key" setx
GROQ_MODEL "llama-3.1-8b-instant"

Mac/Linux: export GROQ_API_KEY="your_groq_api_key" export
GROQ_MODEL="llama-3.1-8b-instant"

Restart terminal after setting environment variables.

------------------------------------------------------------------------

### 5️⃣ Run Backend

uvicorn app.main:app --reload

Access API Docs: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

### 6️⃣ Run Streamlit UI (Optional)

streamlit run ui.py

------------------------------------------------------------------------

## 📈 Example API Flow

1.  POST /api/v1/auth/login → Get JWT
2.  POST /api/v1/ingest → Upload document
3.  POST /api/v1/query → Ask question (with Bearer token)

------------------------------------------------------------------------

## 🛡 Production Design Considerations

-   Retry & fallback model strategy
-   Prompt versioning
-   Confidence-based rejection
-   Soft deletes instead of vector mutation
-   Configurable model selection via environment variables

------------------------------------------------------------------------

## 📌 Future Enhancements

-   Hybrid Search (BM25 + Vector)
-   Multi-tenant isolation
-   Offline evaluation dataset
-   Cost tracking dashboard

------------------------------------------------------------------------

## 📄 License

For educational and demonstration purposes.
