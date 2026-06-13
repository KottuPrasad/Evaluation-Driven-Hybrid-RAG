# Runs the complete BM25 + Vector + RRF retrieval pipeline.

from retrieval.retrievers.bm25_retriever import BM25Retriever

from retrieval.retrievers.vector_retriever import VectorRetriever

from retrieval.rrf_fusion import RRFFusion


class HybridRRFRetriever:

    def __init__(self):

        self.bm25_retriever = BM25Retriever()

        self.vector_retriever = VectorRetriever()

        self.rrf = RRFFusion()

    def search(
        self,
        query,
        bm25,
        index,
        chunks,
        retrieval_top_k=8,
        final_top_k=5
    ):

        bm25_results = self.bm25_retriever.search(
            query=query,
            bm25=bm25,
            chunks=chunks,
            top_k=retrieval_top_k
        )

        vector_results = self.vector_retriever.search(
            query=query,
            index=index,
            chunks=chunks,
            top_k=retrieval_top_k
        )

        fused_results = self.rrf.fuse(
            bm25_results=bm25_results,
            vector_results=vector_results,
            top_k=final_top_k
        )

        return fused_results