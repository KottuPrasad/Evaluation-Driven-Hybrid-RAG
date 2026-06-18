import json
from collections import defaultdict

from retrieval.query_processor import (
    QueryProcessor
)


query_processor = (
    QueryProcessor()
)


with open(
    "evaluation/datasets/Evaluation_dataset.json",
    "r",
    encoding="utf-8"
) as f:

    dataset = json.load(f)


total = 0
correct = 0

mistakes = []

class_total = defaultdict(int)
class_correct = defaultdict(int)


for item in dataset:

    query = item["query"]

    actual_type = item[
        "query_type"
    ]

    processed_query = (
        query_processor.process(
            query
        )
    )

    predicted_type = (
        processed_query[
            "query_type"
        ]
    )

    total += 1

    class_total[
        actual_type
    ] += 1

    if predicted_type == actual_type:

        correct += 1

        class_correct[
            actual_type
        ] += 1

    else:

        mistakes.append(
            {
                "query": query,
                "actual": actual_type,
                "predicted": predicted_type
            }
        )


accuracy = correct / total


print(
    "\n===== OVERALL ROUTING ACCURACY ====="
)

print(
    f"\nCorrect: {correct}/{total}"
)

print(
    f"Accuracy: {accuracy:.4f}"
)


print(
    "\n===== PER-TYPE ACCURACY ====="
)

for query_type in sorted(
    class_total.keys()
):

    acc = (
        class_correct[
            query_type
        ]
        /
        class_total[
            query_type
        ]
    )

    print(
        f"{query_type}: "
        f"{class_correct[query_type]}"
        f"/{class_total[query_type]}"
        f" ({acc:.4f})"
    )


print(
    "\n===== MISCLASSIFICATIONS ====="
)

if len(mistakes) == 0:

    print(
        "\nNo routing mistakes."
    )

else:

    for mistake in mistakes:

        print(
            "\nQuery:",
            mistake["query"]
        )

        print(
            "Actual:",
            mistake["actual"]
        )

        print(
            "Predicted:",
            mistake["predicted"]
        )