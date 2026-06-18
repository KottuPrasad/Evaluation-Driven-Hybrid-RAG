import json
import pickle
import faiss

from evaluation.metrics import (
    EvaluationMetrics
)

from retrieval.query_processor import (
    QueryProcessor
)

from retrieval.retrievers.bm25_retriever import (
    BM25Retriever
)

from retrieval.retrievers.vector_retriever import (
    VectorRetriever
)

from retrieval.rrf_fusion import (
    RRFFusion
)

from retrieval.cross_encoder_reranker import (
    CrossEncoderReranker
)


class RoutingEvaluator:

    def __init__(self):

        self.metrics = (
            EvaluationMetrics()
        )

        self.query_processor = (
            QueryProcessor()
        )

        self.bm25_retriever = (
            BM25Retriever()
        )

        self.vector_retriever = (
            VectorRetriever()
        )

        self.rrf = RRFFusion()

        self.cross_encoder = (
            CrossEncoderReranker()
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
            "evaluation/datasets/Evaluation_dataset.json",
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(
                f
            )

    def filter_version_chunks(
        self,
        chunks,
        version
    ):

        if not version:

            return chunks

        filtered = []

        for chunk in chunks:

            searchable_text = f"""
            {chunk.get('title', '')}
            {chunk.get('section', '')}
            {chunk.get('subsection', '')}
            {chunk.get('text', '')}
            """

            if (
                version.lower()
                in searchable_text.lower()
            ):

                filtered.append(
                    chunk
                )

        if len(filtered) > 0:

            return filtered

        return chunks
    
    def filter_mixed_chunks(
        self,
        chunks,
        version
    ):

        if not version:

            return chunks

        documentation_chunks = []

        release_note_chunks = []

        for chunk in chunks:

            if (
                chunk.get(
                    "file_name",
                    ""
                )
                == "release-notes.md"
            ):

                release_note_chunks.append(
                    chunk
                )

            else:

                documentation_chunks.append(
                    chunk
                )

        filtered_release_notes = (
            self.filter_version_chunks(
                release_note_chunks,
                version
            )
        )

        keep_ids = (
            {
                chunk["chunk_id"]
                for chunk in documentation_chunks
            }
            |
            {
                chunk["chunk_id"]
                for chunk in filtered_release_notes
            }
        )

        return [

            chunk

            for chunk in chunks

            if chunk["chunk_id"]
            in keep_ids
        ]

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
        routing_correct = 0
        routing_mistakes = []

        for item in dataset:

            query = item["query"]

            difficulty = item[
                "difficulty"
            ]
            
            actual_query_type = item["query_type"]

            relevant_chunk_ids = [

                str(chunk_id)

                for chunk_id in item[
                    "relevant_chunk_ids"
                ]
            ]

            processed_query = (
                self.query_processor.process(
                    query
                )
            )

            query_type = (
                processed_query[
                    "query_type"
                ]
            )
            
            if query_type == actual_query_type:

                routing_correct += 1

            else:

                routing_mistakes.append(
                    {
                        "query": query,
                        "actual_query_type": actual_query_type,
                        "predicted_query_type": query_type
                    }
                )

            version = (
                processed_query[
                    "version"
                ]
            )

            normalized_query = (
                processed_query[
                    "normalized_query"
                ]
            )

            if (
                query_type
                == "release_notes"
            ):

                bm25_results = (
                    self.bm25_retriever.search(
                        query=normalized_query,
                        bm25=bm25,
                        chunks=chunks,
                        top_k=20
                    )
                )

                filtered_bm25 = (
                    self.filter_version_chunks(
                        bm25_results,
                        version
                    )
                )

                final_chunks = (
                    filtered_bm25[:8]
                )

            elif(
                query_type
                == "mixed"
            ):

                bm25_results = (
                    self.bm25_retriever.search(
                        query=normalized_query,
                        bm25=bm25,
                        chunks=chunks,
                        top_k=15
                    )
                )

                vector_results = (
                    self.vector_retriever.search(
                        query=normalized_query,
                        index=index,
                        chunks=chunks,
                        top_k=15
                    )
                )

                rrf_results = (
                    self.rrf.fuse(
                        bm25_results=bm25_results,
                        vector_results=vector_results,
                        top_k=15
                    )
                )

                filtered_rrf = (
                    self.filter_mixed_chunks(
                        rrf_results,
                        version
                    )
                )

                final_chunks = (
                    filtered_rrf[:8]
                )
            else:

                bm25_results = (
                    self.bm25_retriever.search(
                        query=normalized_query,
                        bm25=bm25,
                        chunks=chunks,
                        top_k=15
                    )
                )

                vector_results = (
                    self.vector_retriever.search(
                        query=normalized_query,
                        index=index,
                        chunks=chunks,
                        top_k=15
                    )
                )

                rrf_results = (
                    self.rrf.fuse(
                        bm25_results=bm25_results,
                        vector_results=vector_results,
                        top_k=15
                    )
                )

                final_chunks = (
                    self.cross_encoder.rerank(
                        query=normalized_query,
                        chunks=rrf_results,
                        top_k=8
                    )
                )

            retrieved_chunk_ids = [

                str(chunk["chunk_id"])

                for chunk in final_chunks
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

            total_hit_rate += hit_rate
            total_recall += recall
            total_mrr += mrr
            

            query_results.append({

                "query":
                query,

                "actual_query_type":
                actual_query_type,

                "predicted_query_type":
                query_type,

                "difficulty":
                difficulty,

                "relevant_chunk_ids":
                relevant_chunk_ids,

                "retrieved_chunk_ids":
                retrieved_chunk_ids,

                "hit_rate":
                round(hit_rate, 4),

                "recall":
                round(recall, 4),

                "mrr":
                round(mrr, 4)
            })

        total_queries = len(
            dataset
        )

        routing_accuracy = (
        routing_correct
        / total_queries
        )
        
        summary = {

            "total_queries":
            total_queries,

            "routing_accuracy":
            round(
                routing_accuracy,
                4
            ),

            "routing_correct":
            routing_correct,

            "routing_total":
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

            "routing_mistakes":
            routing_mistakes,

            "query_results":
            query_results
        }

        with open(
            "evaluation/results/routing_pipeline_summary.json",
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
        RoutingEvaluator()
    )

    evaluator.evaluate()