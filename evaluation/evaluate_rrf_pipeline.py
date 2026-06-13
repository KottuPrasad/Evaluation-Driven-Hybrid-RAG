import json
import pickle
import faiss

from evaluation.metrics import EvaluationMetrics

from retrieval.pipelines.rrf_retriever import (
    HybridRRFRetriever
)


class RRFEvaluator:

    def __init__(self):

        self.metrics = (
            EvaluationMetrics()
        )

        self.retriever = (
            HybridRRFRetriever()
        )

    def load_resources(self):

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

    def load_dataset(self):

        with open(
            "evaluation/datasets/clean_query_dataset.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(
                f
            )

    def evaluate(self):

        chunks, bm25, index = (
            self.load_resources()
        )

        dataset = (
            self.load_dataset()
        )

        query_results = []

        total_hit_rate = 0
        total_recall = 0
        total_mrr = 0

        for item in dataset:

            query = item["query"]

            difficulty = item[
                "difficulty"
            ]

            relevant_chunk_ids = [
                str(chunk_id)
                for chunk_id in item[
                    "relevant_chunk_ids"
                ]
            ]

            results = (
                self.retriever.search(
                    query=query,
                    bm25=bm25,
                    index=index,
                    chunks=chunks,
                    retrieval_top_k=8,
                    final_top_k=5
                )
            )

            retrieved_chunk_ids = [

                chunk["chunk_id"]

                for chunk in results
            ]

            hit_rate = (
                self.metrics.hit_rate_at_k(
                    retrieved_chunk_ids,
                    relevant_chunk_ids
                )
            )

            recall = (
                self.metrics.recall_at_k(
                    retrieved_chunk_ids,
                    relevant_chunk_ids
                )
            )

            mrr = (
                self.metrics.mrr(
                    retrieved_chunk_ids,
                    relevant_chunk_ids
                )
            )

            total_hit_rate += (
                hit_rate
            )

            total_recall += (
                recall
            )

            total_mrr += (
                mrr
            )

            query_results.append({

                "query": query,

                "difficulty": difficulty,

                "relevant_chunk_ids":
                relevant_chunk_ids,

                "retrieved_chunk_ids":
                retrieved_chunk_ids,

                "hit_rate":
                round(
                    hit_rate,
                    4
                ),

                "recall":
                round(
                    recall,
                    4
                ),

                "mrr":
                round(
                    mrr,
                    4
                )
            })

        total_queries = len(
            dataset
        )

        summary = {

            "total_queries":
            total_queries,

            "average_hit_rate":
            round(
                total_hit_rate
                / total_queries,
                4
            ),

            "average_recall":
            round(
                total_recall
                / total_queries,
                4
            ),

            "average_mrr":
            round(
                total_mrr
                / total_queries,
                4
            )
        }

        final_results = {

            "summary":
            summary,

            "query_results":
            query_results
        }

        with open(
            "evaluation/results/rrf_pipeline_summary.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                final_results,
                f,
                indent=4
            )

        print(
            "\nEvaluation Complete."
        )

        print(
            "\nSummary:"
        )

        print(
            json.dumps(
                summary,
                indent=4
            )
        )


if __name__ == "__main__":

    evaluator = (
        RRFEvaluator()
    )

    evaluator.evaluate()