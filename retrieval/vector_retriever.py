from config.settings import EMBEDDING_MODEL


class VectorRetriever:

    def __init__(self):

        self.model = EMBEDDING_MODEL

    def search(
        self,
        query,
        index,
        chunks,
        top_k=5
    ):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        scores, indices = index.search(
            query_embedding.astype(
                "float32"
            ),
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            chunk = chunks[idx].copy()

            chunk["score"] = float(
                score
            )

            results.append(
                chunk
            )

        return results