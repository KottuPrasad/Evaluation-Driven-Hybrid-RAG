import json
import pickle
import faiss

from evaluation.metrics import EvaluationMetrics

from retrieval.query_processor import (
    QueryNormalizer
)

from retrieval.pipelines.cross_encoder_retriever import (
    HybridCrossEncoderRetriever
)


class QueryNormalizerEvaluator:

    def __init__(self):

        self.metrics = (
            EvaluationMetrics()
        )

        self.normalizer = (
            QueryNormalizer()
        )

        self.retriever = (
            HybridCrossEncoderRetriever()
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
            "evaluation/datasets/noisy_query_dataset.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(
                f
            )

    def calculate_metrics(
        self,
        dataset,
        chunks,
        bm25,
        index,
        use_normalizer
    ):

        total_hit_rate = 0
        total_recall = 0
        total_mrr = 0

        query_results = []

        for item in dataset:

            original_query = (
                item["query"]
            )

            relevant_chunk_ids = [

                str(chunk_id)

                for chunk_id in item[
                    "relevant_chunk_ids"
                ]
            ]

            if use_normalizer:

                final_query = (
                    self.normalizer.normalize(
                        original_query
                    )
                )

            else:

                final_query = (
                    original_query
                )

            results = (

                self.retriever.search(
                    query=final_query,
                    bm25=bm25,
                    index=index,
                    chunks=chunks,
                    retrieval_top_k=8,
                    rrf_top_k=10,
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

                "original_query":
                original_query,

                "final_query":
                final_query,

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

        return {

            "summary":
            summary,

            "query_results":
            query_results
        }

    def evaluate(self):

        chunks, bm25, index = (
            self.load_resources()
        )

        dataset = (
            self.load_dataset()
        )

        without_normalizer = (

            self.calculate_metrics(
                dataset=dataset,
                chunks=chunks,
                bm25=bm25,
                index=index,
                use_normalizer=False
            )

        )

        with_normalizer = (

            self.calculate_metrics(
                dataset=dataset,
                chunks=chunks,
                bm25=bm25,
                index=index,
                use_normalizer=True
            )

        )

        final_results = {

            "without_normalizer":
            without_normalizer,

            "with_normalizer":
            with_normalizer

        }

        with open(
            "evaluation/results/query_normalizer_comparison.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                final_results,
                f,
                indent=4
            )

        print(
            "\nWITHOUT NORMALIZER"
        )

        print(
            json.dumps(
                without_normalizer[
                    "summary"
                ],
                indent=4
            )
        )

        print(
            "\nWITH NORMALIZER"
        )

        print(
            json.dumps(
                with_normalizer[
                    "summary"
                ],
                indent=4
            )
        )


if __name__ == "__main__":

    evaluator = (
        QueryNormalizerEvaluator()
    )

    evaluator.evaluate()