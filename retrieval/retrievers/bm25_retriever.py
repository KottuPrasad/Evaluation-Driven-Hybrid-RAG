# Retrieves chunks using BM25 keyword-based search.

import re

import numpy as np

from nltk.corpus import stopwords


class BM25Retriever:

    def __init__(self):

        self.stopwords = set(
            stopwords.words(
                "english"
            )
        )

    def tokenize(
        self,
        text
    ):

        tokens = re.findall(
            r"\b\w+\b",
            text.lower()
        )

        filtered_tokens = []

        for token in tokens:

            if token not in self.stopwords:

                filtered_tokens.append(
                    token
                )

        return filtered_tokens

    def search(
        self,
        query,
        bm25,
        chunks,
        top_k=5
    ):

        query_tokens = self.tokenize(
            query
        )

        scores = bm25.get_scores(
            query_tokens
        )

        ranked_indices = np.argsort(
            scores
        )[::-1]

        if max(scores) <= 0:
            return []

        top_indices = ranked_indices[
            :top_k
        ]

        results = []

        for idx in top_indices:

            chunk = chunks[idx].copy()

            chunk["score"] = float(
                scores[idx]
            )

            results.append(
                chunk
            )

        return results