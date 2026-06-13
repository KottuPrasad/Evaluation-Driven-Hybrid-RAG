import pickle
import faiss

from retrieval.query_processor import (
    QueryProcessor
)

from retrieval.retrievers.bm25_retriever import (
    BM25Retriever
)

from retrieval.retrievers.vector_retriever import (
    VectorRetriever
)

from retrieval.rrf_fusion import (
    RRFFusion
)

from retrieval.cross_encoder_reranker import (
    CrossEncoderReranker
)

from llm.generator import (
    ResponseGenerator
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


def print_chunks(
    title,
    chunks,
    score_field="score"
):

    print(
        "\n" + "=" * 100
    )

    print(title)

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

        if score_field in chunk:

            print(
                f"Score: "
                f"{chunk[score_field]:.4f}"
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

        if rank <= 2:

            print(
                "\nFULL CHUNK TEXT:\n"
            )

            print(
                chunk["text"]
            )

        print(
            "\n" + "-" * 100
        )

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

        if version.lower() in searchable_text.lower():

            filtered.append(
                chunk
            )

    if len(filtered) > 0:

        return filtered

    return chunks

def main():

    print(
        "\nLoading resources..."
    )

    chunks, bm25, index = (
        load_resources()
    )

    release_notes_count = 0

    release_notes_ids = []

    for chunk in chunks:

        if (
            chunk["title"]
            == "Release Notes"
        ):

            release_notes_count += 1

            release_notes_ids.append(
                chunk["chunk_id"]
            )

    print(
        f"\nRelease Notes Chunks: "
        f"{release_notes_count}"
    )

    print(
        f"Percentage: "
        f"{round(release_notes_count / len(chunks) * 100, 2)}%"
    )

    print(
        f"\nLoaded {len(chunks)} chunks."
    )

    print(
        "\nFirst 10 Release Note Chunks:"
    )

    print(
        release_notes_ids[:10]
    )

    query_processor = (
        QueryProcessor()
    )

    bm25_retriever = (
        BM25Retriever()
    )

    vector_retriever = (
        VectorRetriever()
    )

    rrf = RRFFusion()

    cross_encoder = (
        CrossEncoderReranker()
    )

    generator = (
        ResponseGenerator()
    )

    while True:

        query = input(
            "\nQuery (type exit to quit): "
        )

        if (
            query.lower()
            == "exit"
        ):
            break

        print(
            "\n" + "=" * 100
        )

        print(
            "QUERY ANALYSIS"
        )

        print(
            "=" * 100
        )

        processed_query = (
            query_processor.process(
                query
    )
)

        query_type = (
            processed_query[
                "query_type"
            ]
        )

        version = (
            processed_query[
                "version"
            ]
        )

        normalized_query = (
            processed_query[
                "normalized_query"
            ]
        )

        print(
            f"\nQuery Type: "
            f"{query_type}"
        )

        print(
            f"Version: "
            f"{version}"
        )

        print(
            f"\nOriginal Query: "
            f"{query}"
        )

        print(
            f"Normalized Query: "
            f"{normalized_query}"
        )

        # ============================================================
# RELEASE NOTES ROUTE
# ============================================================

        if query_type == "release_notes":

            print(
                "\nROUTE SELECTED: RELEASE NOTES"
            )

            bm25_results = (
                bm25_retriever.search(
                    query=normalized_query,
                    bm25=bm25,
                    chunks=chunks,
                    top_k=20
                )
            )

            print_chunks(
                "BM25 RESULTS",
                bm25_results
            )

            filtered_bm25 = (
                filter_version_chunks(
                    bm25_results,
                    version
                )
            )

            print_chunks(
                "VERSION FILTERED BM25",
                filtered_bm25
            )

            final_chunks = (
                filtered_bm25[:5]
            )

        # ============================================================
        # MIXED ROUTE
        # ============================================================

        elif query_type == "mixed":

            print(
                "\nROUTE SELECTED: MIXED"
            )

            bm25_results = (
                bm25_retriever.search(
                    query=normalized_query,
                    bm25=bm25,
                    chunks=chunks,
                    top_k=8
                )
            )

            print_chunks(
                "BM25 RESULTS",
                bm25_results
            )

            vector_results = (
                vector_retriever.search(
                    query=normalized_query,
                    index=index,
                    chunks=chunks,
                    top_k=8
                )
            )

            print_chunks(
                "VECTOR RESULTS",
                vector_results
            )

            rrf_results = (
                rrf.fuse(
                    bm25_results=bm25_results,
                    vector_results=vector_results,
                    top_k=10
                )
            )

            print_chunks(
                "RRF RESULTS",
                rrf_results,
                score_field="rrf_score"
            )

            filtered_rrf = (
                filter_version_chunks(
                    rrf_results,
                    version
                )
            )

            print_chunks(
                "VERSION FILTERED RRF",
                filtered_rrf,
                score_field="rrf_score"
            )

            final_chunks = (
                filtered_rrf[:5]
            )

        # ============================================================
        # DOCUMENTATION ROUTE
        # ============================================================

        else:

            print(
                "\nROUTE SELECTED: DOCUMENTATION"
            )

            bm25_results = (
                bm25_retriever.search(
                    query=normalized_query,
                    bm25=bm25,
                    chunks=chunks,
                    top_k=8
                )
            )

            print_chunks(
                "BM25 RESULTS",
                bm25_results
            )

            vector_results = (
                vector_retriever.search(
                    query=normalized_query,
                    index=index,
                    chunks=chunks,
                    top_k=8
                )
            )

            print_chunks(
                "VECTOR RESULTS",
                vector_results
            )

            rrf_results = (
                rrf.fuse(
                    bm25_results=bm25_results,
                    vector_results=vector_results,
                    top_k=10
                )
            )

            print_chunks(
                "RRF RESULTS",
                rrf_results,
                score_field="rrf_score"
            )

            final_chunks = (
                cross_encoder.rerank(
                    query=normalized_query,
                    chunks=rrf_results,
                    top_k=5
                )
            )

            print_chunks(
                "CROSS ENCODER RESULTS",
                final_chunks,
                score_field="cross_encoder_score"
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
    
    
