from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.schemas import (
    QueryRequest,
    QueryResponse
)

from rag_pipeline import (
    RAGPipeline
)

app = FastAPI(
    title="Hybrid RAG API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = RAGPipeline()


@app.get("/")
def root():

    return {
        "message":
        "Hybrid RAG Backend Running"
    }


@app.get("/health")
def health():

    return {
        "status":
        "healthy"
    }


@app.get("/metrics")
def metrics():

    return {

        "embedding_model":
        "BAAI/bge-small-en-v1.5",

        "retrieval":
        "BM25 + Vector + RRF + Cross Encoder",

        "query_routing":
        True
    }


@app.post(
    "/ask",
    response_model=QueryResponse
)
def ask(
    request: QueryRequest
):

    result = pipeline.ask(
        request.query
    )

    return result