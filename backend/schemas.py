from pydantic import BaseModel

from typing import List, Dict, Any


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    query_type: str
    version: str | None
    normalized_query: str
    route: str

    pipeline: List[Dict[str, Any]]

    sources: List[Dict[str, Any]]