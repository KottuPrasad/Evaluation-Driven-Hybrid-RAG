# Runs the complete BM25 + Vector + RRF + Cross Encoder retrieval pipeline.

from retrieval.retrievers.bm25_retriever import BM25Retriever

from retrieval.retrievers.vector_retriever import VectorRetriever

from retrieval.rrf_fusion import RRFFusion

from retrieval.cross_encoder_reranker import (
    CrossEncoderReranker
)


class HybridCrossEncoderRetriever:

    def __init__(self):

        self.bm25_retriever = BM25Retriever()

        self.vector_retriever = VectorRetriever()

        self.rrf = RRFFusion()

        self.cross_encoder = (
            CrossEncoderReranker()
        )

    def search(
        self,
        query,
        bm25,
        index,
        chunks,
        retrieval_top_k=8,
        rrf_top_k=10,
        final_top_k=5
    ):

        bm25_results = (
            self.bm25_retriever.search(
                query=query,
                bm25=bm25,
                chunks=chunks,
                top_k=retrieval_top_k
            )
        )

        vector_results = (
            self.vector_retriever.search(
                query=query,
                index=index,
                chunks=chunks,
                top_k=retrieval_top_k
            )
        )

        rrf_results = (
            self.rrf.fuse(
                bm25_results=bm25_results,
                vector_results=vector_results,
                top_k=rrf_top_k
            )
        )

        print("\n===== RRF RESULTS =====\n")

        for rank, chunk in enumerate(
            rrf_results,
            start=1
        ):

            print(
                f"Rank: {rank}"
            )

            print(
                f"Title: {chunk['title']}"
            )

            print(
                f"Section: {chunk['section']}"
            )

            print(
                f"Subsection: {chunk['subsection']}"
            )

            print()

            print(
                chunk["text"][:250]
            )

            print(
                "\n" + "=" * 80
            )

        final_results = (
            self.cross_encoder.rerank(
                query=query,
                chunks=rrf_results,
                top_k=final_top_k
            )
        )

        return final_results