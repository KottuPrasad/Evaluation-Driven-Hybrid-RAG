import pickle
import re

from rank_bm25 import BM25Okapi


class BM25Store:

    def tokenize(
        self,
        text
    ):

        return re.findall(
            r"\b\w+\b",
            text.lower()
        )

    def build_corpus(
        self,
        chunks
    ):

        corpus = []

        for chunk in chunks:

            text = f"""
Title: {chunk['title']}
Title: {chunk['title']}
Title: {chunk['title']}

Section: {chunk['section']}
Section: {chunk['section']}

Subsection: {chunk['subsection']}
Subsection: {chunk['subsection']}

Content:
{chunk['text']}
"""

            corpus.append(
                self.tokenize(
                    text
                )
            )

        return corpus

    def create_bm25(
        self,
        chunks
    ):

        corpus = self.build_corpus(
            chunks
        )

        bm25 = BM25Okapi(
            corpus
        )

        return bm25

    def save_bm25(
        self,
        bm25,
        path="vector_db/bm25.pkl"
    ):

        with open(
            path,
            "wb"
        ) as file:

            pickle.dump(
                bm25,
                file
            )

    def load_bm25(
        self,
        path="vector_db/bm25.pkl"
    ):

        with open(
            path,
            "rb"
        ) as file:

            return pickle.load(
                file
            )

    def save_chunks(
        self,
        chunks,
        path="vector_db/chunks.pkl"
    ):

        with open(
            path,
            "wb"
        ) as file:

            pickle.dump(
                chunks,
                file
            )

    def load_chunks(
        self,
        path="vector_db/chunks.pkl"
    ):

        with open(
            path,
            "rb"
        ) as file:

            return pickle.load(
                file
            )