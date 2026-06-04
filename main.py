from retrieval.vector_store import VectorStore
from retrieval.vector_retriever import VectorRetriever

from llm.generator import ResponseGenerator

from config.settings import TOP_K


vector_store = VectorStore()

print(
    "\nLoading vector database..."
)

index = vector_store.load_index()

chunks = vector_store.load_chunks()

print(
    f"\nLoaded {len(chunks)} chunks."
)


retriever = VectorRetriever()

generator = ResponseGenerator()


while True:

    query = input(
        "\nAsk a question (type exit to quit): "
    )

    if query.lower() in [
        "exit",
        "quit"
    ]:

        print(
            "\nGoodbye."
        )

        break

    retrieved_chunks = retriever.search(
        query=query,
        index=index,
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