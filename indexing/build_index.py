from ingestion.markdown_loader import MarkdownLoader
from ingestion.markdown_cleaner import MarkdownCleaner

from chunking.chunker import Chunker

from indexing.vector_store import VectorStore


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


vector_store = VectorStore()

print(
    "\nGenerating embeddings..."
)

embeddings = vector_store.generate_embeddings(
    chunks
)

print(
    "\nCreating FAISS index..."
)

index = vector_store.create_faiss_index(
    embeddings
)

vector_store.save_index(
    index
)

vector_store.save_chunks(
    chunks
)

print(
    "\nVector database saved successfully."
)