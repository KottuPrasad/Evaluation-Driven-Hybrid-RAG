import pickle
import faiss

from retrieval.pipelines.cross_encoder_retriever import (
    HybridCrossEncoderRetriever
)


def load_resources():

    with open(
        "vector_db/chunks.pkl",
        "rb"
    ) as f:

        chunks = pickle.load(
            f
        )

    with open(
        "vector_db/bm25.pkl",
        "rb"
    ) as f:

        bm25 = pickle.load(
            f
        )

    index = faiss.read_index(
        "vector_db/faiss.index"
    )

    return (
        chunks,
        bm25,
        index
    )


def print_results(
    results
):

    print(
        "\n===== CROSS ENCODER RESULTS =====\n"
    )

    for rank, chunk in enumerate(
        results,
        start=1
    ):

        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )

        print()

        print(
            f"Rank: {rank}"
        )

        print(
            f"Cross Encoder Score: "
            f"{chunk['cross_encoder_score']:.4f}"
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
            "Text Preview:\n"
        )

        print(
            chunk["text"][:500]
        )

        print(
            "\n" +
            "=" * 80
        )


def main():

    chunks, bm25, index = (
        load_resources()
    )

    retriever = (
        HybridCrossEncoderRetriever()
    )

    while True:

        query = input(
            "\nAsk a question (type 'exit' to quit): "
        )

        if (
            query.lower()
            == "exit"
        ):
            break

        results = (
            retriever.search(
                query=query,
                bm25=bm25,
                index=index,
                chunks=chunks,
                retrieval_top_k=8,
                rrf_top_k=10,
                final_top_k=5
            )
        )

        print_results(
            results
        )


if __name__ == "__main__":

    main()