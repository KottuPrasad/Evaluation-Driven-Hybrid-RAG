import re
import pickle

from retrieval.query_processor import (
    QueryNormalizer
)

from retrieval.retrievers.bm25_retriever import (
    BM25Retriever
)

from llm.generator import (
    ResponseGenerator
)


def extract_version(
    query
):

    match = re.search(
        r"\d+\.\d+\.\d+",
        query
    )

    if match:

        return (
            match.group()
        )

    return None


def filter_version_chunks(
    chunks,
    version
):

    if not version:

        return chunks

    filtered = []

    for chunk in chunks:

        searchable_text = f"""
{chunk.get('title', '')}
{chunk.get('section', '')}
{chunk.get('subsection', '')}
{chunk.get('text', '')}
"""

        if version in searchable_text:

            filtered.append(
                chunk
            )

    if len(filtered) > 0:

        return filtered

    return chunks


def print_chunks(
    title,
    chunks
):

    print(
        "\n" + "=" * 100
    )

    print(
        title
    )

    print(
        "=" * 100
    )

    for rank, chunk in enumerate(
        chunks,
        start=1
    ):

        print(
            f"\nRank: {rank}"
        )

        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )

        print(
            f"Score: {chunk['score']:.4f}"
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

        print(
            "\nFULL CHUNK TEXT:\n"
        )

        print(
            chunk["text"]
        )

        print(
            "\n" + "-" * 100
        )


def main():

    print(
        "\nLoading resources..."
    )

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

    print(
        f"\nLoaded {len(chunks)} chunks."
    )

    normalizer = (
        QueryNormalizer()
    )

    retriever = (
        BM25Retriever()
    )

    generator = (
        ResponseGenerator()
    )

    while True:

        query = input(
            "\nRelease Notes Query (type exit to quit): "
        )

        if (
            query.lower()
            == "exit"
        ):
            break

        version = (
            extract_version(
                query
            )
        )

        print(
            f"\nDetected Version: "
            f"{version}"
        )

        normalized_query = (
            normalizer.normalize(
                query
            )
        )

        print(
            f"\nNormalized Query: "
            f"{normalized_query}"
        )

        bm25_results = (
            retriever.search(
                query=normalized_query,
                bm25=bm25,
                chunks=chunks,
                top_k=20
            )
        )

        print_chunks(
            "BM25 TOP 20 RESULTS",
            bm25_results
        )

        filtered_results = (
            filter_version_chunks(
                bm25_results,
                version
            )
        )

        print_chunks(
            "VERSION FILTERED RESULTS",
            filtered_results
        )

        final_chunks = (
            filtered_results[:5]
        )

        answer = (
            generator.generate_answer(
                query=normalized_query,
                retrieved_chunks=final_chunks
            )
        )

        print(
            "\n" + "=" * 100
        )

        print(
            "FINAL ANSWER"
        )

        print(
            "=" * 100
        )

        print(
            answer
        )


if __name__ == "__main__":

    main()