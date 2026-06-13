import json

with open(
    "evaluation/evaluation_dataset.json",
    "r"
) as f:

    data = json.load(f)

print(
    data[0]["relevant_chunk_ids"][0]
)

print(
    type(
        data[0]["relevant_chunk_ids"][0]
    )
)