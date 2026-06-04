# Evaluation-Driven Hybrid RAG System

## Overview

This project is an Evaluation-Driven Hybrid Retrieval-Augmented Generation (RAG) system built using FastAPI documentation as the knowledge base.

The project explores and compares multiple retrieval approaches:

* Vector Retrieval using FAISS and Sentence Transformers
* BM25 Keyword Retrieval
* Hybrid Retrieval (Upcoming)
* Reciprocal Rank Fusion (RRF) (Upcoming)

The goal is not simply to build a chatbot, but to evaluate retrieval quality, analyze retrieval behavior, and compare retrieval strategies using benchmark queries and retrieval metrics.

---

## Current Features

### Data Ingestion

* Markdown document loading
* Documentation cleaning and preprocessing
* FastAPI documentation corpus

### Chunking

* Structure-aware chunking
* Metadata extraction:

  * Title
  * Section
  * Subsection

### Vector Retrieval

* BAAI/bge-small-en-v1.5 embeddings
* FAISS vector index
* Persistent vector database
* Top-K semantic retrieval

### BM25 Retrieval

* BM25 keyword search
* Metadata-weighted corpus construction
* Query preprocessing with stopword removal
* Persistent BM25 index

### Generation

* Groq LLM integration
* Context-grounded answer generation
* Hallucination reduction through prompt engineering

### Evaluation

* Manual benchmark queries
* Retrieval quality analysis
* Failure analysis and iterative improvement

---

## Project Structure

```text
Project1/
│
├── chunking/
├── config/
├── ingestion/
├── llm/
├── retrieval/
│
├── build_index.py
├── build_bm25.py
├── main.py
├── main_bm25.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Retrieval Pipeline

### Vector Retrieval

Query
→ Embedding Generation
→ FAISS Search
→ Top-K Chunks
→ LLM Generation

### BM25 Retrieval

Query
→ Query Preprocessing
→ BM25 Retrieval
→ Top-K Chunks
→ LLM Generation

---

## Current Status

Completed:

* Document Ingestion
* Chunking
* Metadata Extraction
* Embeddings
* FAISS Retrieval
* BM25 Retrieval
* Retrieval Evaluation

In Progress:

* Hybrid Retrieval
* Reciprocal Rank Fusion (RRF)
* Evaluation Dataset
* Retrieval Metrics

Planned:

* Hybrid Retrieval Benchmarking
* Streamlit Frontend
* Architecture Diagrams
* Project Documentation

---

## Motivation

This project was built to understand retrieval systems in depth and to compare keyword-based and semantic retrieval methods through systematic evaluation rather than relying solely on chatbot outputs.

The focus is on engineering decisions, retrieval quality, benchmarking, and explainability.
