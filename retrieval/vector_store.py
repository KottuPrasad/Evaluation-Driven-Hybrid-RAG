import pickle

import faiss

from config.settings import EMBEDDING_MODEL


class VectorStore:

    def __init__(self):

        self.model = EMBEDDING_MODEL

    def generate_embeddings(
        self,
        chunks
    ):

        texts = []

        for chunk in chunks:

            embedding_text = f"""
Title: {chunk['title']}

Section: {chunk['section']}

Subsection: {chunk['subsection']}

Content:
{chunk['text']}
"""

            texts.append(
                embedding_text.strip()
            )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings

    def create_faiss_index(
        self,
        embeddings
    ):

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(
            embeddings.astype(
                "float32"
            )
        )

        return index

    def save_index(
        self,
        index,
        path="vector_db/faiss.index"
    ):

        faiss.write_index(
            index,
            path
        )

    def load_index(
        self,
        path="vector_db/faiss.index"
    ):

        return faiss.read_index(
            path
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