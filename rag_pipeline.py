import pickle
import faiss

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

from llm.generator import (
    ResponseGenerator
)


class RAGPipeline:

    def __init__(self):

        with open(
            "vector_db/chunks.pkl",
            "rb"
        ) as f:

            self.chunks = pickle.load(
                f
            )

        with open(
            "vector_db/bm25.pkl",
            "rb"
        ) as f:

            self.bm25 = pickle.load(
                f
            )

        self.index = faiss.read_index(
            "vector_db/faiss.index"
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

        self.generator = (
            ResponseGenerator()
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
        rrf_results,
        version
    ):
        
        documentation_chunks = []

        release_note_chunks = []

        for chunk in rrf_results:

            if (
                chunk.get("file_name", "")
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
                c["chunk_id"]
                for c in documentation_chunks
            }
            |
            {
                c["chunk_id"]
                for c in filtered_release_notes
            }
        )

        final_results = [

            chunk

            for chunk in rrf_results

            if chunk["chunk_id"] in keep_ids
        ]

        return final_results

    def build_sources(
        self,
        chunks
    ):

        sources = []

        for chunk in chunks:

            sources.append(

                {
                    "title":
                    chunk.get(
                        "title",
                        ""
                    ),

                    "section":
                    chunk.get(
                        "section",
                        ""
                    ),

                    "subsection":
                    chunk.get(
                        "subsection",
                        ""
                    )
                }

            )

        return sources

    def ask(
        self,
        query
    ):

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

        route = query_type

        if (
            query_type
            == "release_notes"
        ):

            bm25_results = (
                self.bm25_retriever.search(
                    query=normalized_query,
                    bm25=self.bm25,
                    chunks=self.chunks,
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
                filtered_bm25[:5]
            )

        elif (
            query_type
            == "mixed"
        ):

            bm25_results = (
                self.bm25_retriever.search(
                    query=normalized_query,
                    bm25=self.bm25,
                    chunks=self.chunks,
                    top_k=15
                )
            )

            vector_results = (
                self.vector_retriever.search(
                    query=normalized_query,
                    index=self.index,
                    chunks=self.chunks,
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
                    bm25=self.bm25,
                    chunks=self.chunks,
                    top_k=15
                )
            )

            vector_results = (
                self.vector_retriever.search(
                    query=normalized_query,
                    index=self.index,
                    chunks=self.chunks,
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
        answer = (
            self.generator.generate_answer(
                query=normalized_query,
                retrieved_chunks=final_chunks
            )
        )

        if query_type == "release_notes":

            pipeline = [

                {
                    "label":
                    "Query Understanding"
                },

                {
                    "label":
                    "BM25 Retrieval",

                    "meta":
                    "20 Chunks Retrieved"
                },

                {
                    "label":
                    "Version Filter",

                    "meta":
                    "Version-Aware Filtering"
                },

                {
                    "label":
                    "Retrieved Chunks",

                    "meta":
                    "Top 5 Chunks"
                },

                {
                    "label":
                    "Answer Generation"
                }
            ]

        elif query_type == "mixed":

            pipeline = [

                {
                    "label":
                    "Query Understanding"
                },

                {
                    "label":
                    "BM25 Retrieval",

                    "meta":
                    "15 Chunks Retrieved"
                },

                {
                    "label":
                    "Vector Retrieval",

                    "meta":
                    "15 Chunks Retrieved"
                },

                {
                    "label":
                    "RRF Fusion",

                    "meta":
                    "15 Chunks Fused"
                },

                {
                    "label":
                    "Mixed Filter",

                    "meta":
                    "Keep Docs + Filter Release Notes"
                },

                {
                    "label":
                    "Retrieved Chunks",

                    "meta":
                    "Top 8 Chunks"
                },

                {
                    "label":
                    "Answer Generation"
                }
            ]

        else:

            pipeline = [

                {
                    "label":
                    "Query Understanding"
                },

                {
                    "label":
                    "BM25 Retrieval",

                    "meta":
                    "15 Chunks Retrieved"
                },

                {
                    "label":
                    "Vector Retrieval",

                    "meta":
                    "15 Chunks Retrieved"
                },

                {
                    "label":
                    "RRF Fusion",

                    "meta":
                    "15 Chunks Fused"
                },

                {
                    "label":
                    "Cross Encoder",

                    "meta":
                    "8 Chunks Reranked"
                },

                {
                    "label":
                    "Answer Generation"
                }
            ]

        return {

            "answer":
            answer,

            "query_type":
            query_type,

            "version":
            version,

            "normalized_query":
            normalized_query,

            "route":
            route,

            "pipeline":
            pipeline,

            "sources":
            self.build_sources(
                final_chunks
            )
        }