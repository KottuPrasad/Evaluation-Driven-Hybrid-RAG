from retrieval.retrievers.bm25_retriever import BM25Retriever
from retrieval.retrievers.vector_retriever import VectorRetriever

class HybridRetriever:
    
    def __init__(self):
        
        self.bm25_retriever = BM25Retriever()
        
        self.vector_retriever = VectorRetriever()
        
    def search(
        self,
        query,
        bm25,
        index,
        chunks,
        top_k=8
    ):
        
        bm25_results = self.bm25_retriever.search(
            query=query,
            bm25=bm25,
            chunks=chunks,
            top_k=top_k
        )
        
        vector_results = self.vector_retriever.search(
            query=query,
            index=index,
            chunks=chunks,
            top_k=top_k
        )
        
        return {
            "bm25_results":bm25_results,
            "vector_results":vector_results
        }