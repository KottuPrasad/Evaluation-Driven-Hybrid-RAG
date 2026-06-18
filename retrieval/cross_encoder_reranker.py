# Re-ranks retrieved chunks using a Cross Encoder for better relevance.

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

    def rerank(
        self,
        query,
        chunks,
        top_k=5
    ):

        pairs = []

        for chunk in chunks:

            rerank_text = f"""
        Title: {chunk.get('title', '')}
        Section: {chunk.get('section', '')}
        Subsection: {chunk.get('subsection', '')}

        Content:
        {chunk.get('text', '')}
        """

            pairs.append(
                [
                    query,
                    rerank_text
                ]
        )

        scores = self.model.predict(
            pairs
        )

        for chunk, score in zip(
            chunks,
            scores
        ):

            chunk[
                "cross_encoder_score"
            ] = float(score)

        reranked_chunks = sorted(
            chunks,
            key=lambda x:
            x["cross_encoder_score"],
            reverse=True
        )

        return reranked_chunks[
            :top_k
        ]