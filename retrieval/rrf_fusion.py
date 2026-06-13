# Combines BM25 and vector search rankings using Reciprocal Rank Fusion (RRF).

class RRFFusion:

    def __init__(
        self,
        k=60
    ):

        self.k = k

    def fuse(
        self,
        bm25_results,
        vector_results,
        top_k=10
    ):

        rrf_scores = {}

        chunk_lookup = {}

        for rank, chunk in enumerate(
            bm25_results,
            start=1
        ):

            chunk_id = chunk[
                "chunk_id"
            ]

            rrf_score = 1 / (
                self.k + rank
            )

            if chunk_id not in rrf_scores:

                rrf_scores[
                    chunk_id
                ] = 0

                chunk_lookup[
                    chunk_id
                ] = chunk

            rrf_scores[
                chunk_id
            ] += rrf_score

        for rank, chunk in enumerate(
            vector_results,
            start=1
        ):

            chunk_id = chunk[
                "chunk_id"
            ]

            rrf_score = 1 / (
                self.k + rank
            )

            if chunk_id not in rrf_scores:

                rrf_scores[
                    chunk_id
                ] = 0

                chunk_lookup[
                    chunk_id
                ] = chunk

            rrf_scores[
                chunk_id
            ] += rrf_score

        ranked_chunks = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for chunk_id, score in ranked_chunks[
            :top_k
        ]:

            chunk = chunk_lookup[
                chunk_id
            ].copy()

            chunk.pop(
                "score",
                None
            )

            chunk[
                "rrf_score"
            ] = score

            results.append(
                chunk
            )

        return results