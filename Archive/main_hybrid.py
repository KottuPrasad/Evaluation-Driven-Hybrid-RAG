from Archive.hybrid_retriever import HybridRetriever

from indexing.bm25_store import BM25Store

from indexing.vector_store import VectorStore


bm25_store = BM25Store()

vector_store = VectorStore()


bm25 = bm25_store.load_bm25()

index = vector_store.load_index()

chunks = vector_store.load_chunks()


hybrid_retriever = HybridRetriever()


while True:

    query = input(
        "\nAsk a question (type 'exit' to quit): "
    )

    if query.lower() == "exit":

        break

    results = hybrid_retriever.search(
        query=query,
        bm25=bm25,
        index=index,
        chunks=chunks,
        top_k=15
    )

    print(
        "\n===== BM25 RESULTS ====="
    )

    for rank, chunk in enumerate(
        results["bm25_results"],
        start=1
    ):
 
        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )
        
        print(
            f"\nRank: {rank}"
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
            f"\nText Preview:\n"
        )

        print(
            chunk["text"]
        )

        print(
            "\n" + "=" * 80
        )

    print(
        "\n===== VECTOR RESULTS ====="
    )

    for rank, chunk in enumerate(
        results["vector_results"],
        start=1
    ):

        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )
        
        print(
            f"\nRank: {rank}"
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
            f"\nText Preview:\n"
        )

        print(
            chunk["text"]
        )

        print(
            "\n" + "=" * 80
        )