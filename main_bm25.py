from retrieval.bm25_store import BM25Store
from retrieval.bm25_retrieval import BM25Retriever

from llm.generator import ResponseGenerator

from config.settings import TOP_K


bm25_store = BM25Store()

print(
    "\nLoading BM25 database..."
)

bm25 = bm25_store.load_bm25()

chunks = bm25_store.load_chunks()

print(
    f"\nLoaded Chunks: {len(chunks)}"
)


retriever = BM25Retriever()

generator = ResponseGenerator()


while True:

    query = input(
        "\nAsk a question (type 'exit' to quit): "
    )

    if query.lower() == "exit":

        print(
            "\nExiting..."
        )

        break

    retrieved_chunks = retriever.search(
        query=query,
        bm25=bm25,
        chunks=chunks,
        top_k=TOP_K
    )

    print(
        "\n===== RETRIEVED CHUNKS =====\n"
    )

    for rank, chunk in enumerate(
        retrieved_chunks,
        start=1
    ):

        print(
            f"Rank: {rank}"
        )

        print(
            f"Score: {chunk['score']:.4f}"
        )

        print(
            f"Chunk ID: {chunk['chunk_id']}"
        )

        print(
            f"File: {chunk['file_name']}"
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
            "\nText Preview:\n"
        )

        print(
            chunk["text"][:500]
        )

        print(
            "\n" + "=" * 80
        )

    answer = generator.generate_answer(
        query=query,
        retrieved_chunks=retrieved_chunks
    )

    print(
        "\n===== FINAL ANSWER =====\n"
    )

    print(
        answer
    )