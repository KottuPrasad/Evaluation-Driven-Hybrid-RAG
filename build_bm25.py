from ingestion.markdown_loader import MarkdownLoader
from ingestion.markdown_cleaner import MarkdownCleaner

from chunking.chunker import Chunker

from retrieval.bm25_store import BM25Store


loader = MarkdownLoader(
    r"D:\Downloads\fastapi-master\fastapi-master\docs\en\docs"
)

documents = loader.load_documents()

print(
    f"\nLoaded Documents: {len(documents)}"
)


cleaner = MarkdownCleaner()

for document in documents:

    document["content"] = cleaner.clean(
        document["content"]
    )

print(
    "\nDocument cleaning completed."
)


chunker = Chunker()

chunks = chunker.create_chunks(
    documents
)

print(
    f"\nTotal Chunks Created: {len(chunks)}"
)


bm25_store = BM25Store()

print(
    "\nBuilding BM25..."
)

bm25 = bm25_store.create_bm25(
    chunks
)

bm25_store.save_bm25(
    bm25
)

bm25_store.save_chunks(
    chunks
)

print(
    "\nBM25 database saved successfully."
)