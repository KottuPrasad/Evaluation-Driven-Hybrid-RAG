import pickle

with open("vector_db/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print("Total Chunks:", len(chunks))

print("\nFirst Chunk ID:")
print(chunks[0]["chunk_id"])
print(type(chunks[0]["chunk_id"]))