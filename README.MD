# 🚀 Evaluation-Driven Hybrid RAG System for FastAPI Documentation & Release Notes

### Hybrid Retrieval-Augmented Generation using BM25, Dense Retrieval, RRF Fusion, Cross-Encoder Re-ranking, and Adaptive Query Routing

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.137-009688?logo=fastapi\&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange)
![BM25](https://img.shields.io/badge/BM25-Sparse_Retrieval-green)
![Cross Encoder](https://img.shields.io/badge/Cross--Encoder-Re--Ranking-purple)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![Routing Accuracy](https://img.shields.io/badge/Routing_Accuracy-93.33%25-success)

---

## 📖 Overview

This project implements a complete Hybrid Retrieval-Augmented Generation (RAG) system for answering questions over FastAPI Documentation and FastAPI Release Notes.

The system combines BM25 sparse retrieval, dense vector retrieval using FAISS and BGE embeddings, Reciprocal Rank Fusion (RRF), Cross-Encoder re-ranking, and adaptive query routing to improve retrieval quality and answer accuracy.

Users can ask documentation questions, version-specific release note questions, or mixed questions requiring information from both sources. The system automatically identifies query intent and routes each query through the most appropriate retrieval pipeline before generating a final answer.

The project also includes a manually labeled benchmark dataset, an evaluation framework, a FastAPI backend, and a Next.js frontend for interactive querying and retrieval visualization.

---

## 🎯 Project Objectives

* Build a production-style Hybrid RAG pipeline
* Compare sparse and dense retrieval approaches
* Implement retrieval fusion using Reciprocal Rank Fusion (RRF)
* Improve ranking quality through Cross-Encoder re-ranking
* Design adaptive routing for different query categories
* Measure retrieval performance using benchmark-based evaluation
* Develop a complete end-to-end system with frontend and backend integration

---

## ⚡ Key Features

### 🔍 Hybrid Retrieval

Combines:

* BM25 Sparse Retrieval
* Dense Vector Retrieval (FAISS + BGE Embeddings)

to capture both lexical and semantic relevance.

### 🔄 Reciprocal Rank Fusion (RRF)

Fuses sparse and dense retrieval rankings into a unified candidate set.

### 🎯 Cross-Encoder Re-ranking

Applies a Cross-Encoder model to improve ranking quality by directly scoring query-document pairs.

### 🧠 Query Understanding

The system performs:

* Intent Classification
* Query Normalization
* Version Extraction
* Adaptive Retrieval Routing

before retrieval begins.

### 🛣️ Specialized Retrieval Pipelines

Different retrieval strategies are used for:

* Documentation Queries
* Release Notes Queries
* Mixed Queries

instead of forcing every query through a single retrieval pipeline.

### 📊 Evaluation Framework

Includes:

* 30 manually labeled benchmark queries
* Hit Rate@K
* Recall@K
* Mean Reciprocal Rank (MRR)
* Routing Accuracy Evaluation

---

## 📚 Dataset

### Knowledge Sources

The retrieval corpus consists of:

* FastAPI Documentation
* FastAPI Release Notes

### Corpus Statistics

| Source        | Chunks   |
| ------------- | -------- |
| Documentation | 1112     |
| Release Notes | 677      |
| **Total**     | **1789** |

---

## 🏗️ System Architecture

```text
User Query
     │
     ▼
Intent Classification
Version Extraction
Query Normalization
     │
     ▼
Adaptive Routing
     │
     ├──────────────► Documentation Pipeline
     │
     ├──────────────► Release Notes Pipeline
     │
     └──────────────► Mixed Pipeline
                              │
                              ▼
                     Retrieval Pipeline
                              │
                              ▼
                     Response Generation
                              │
                              ▼
                         Final Answer
```

---

## 🔍 Retrieval Pipelines

### Documentation Pipeline

```text
BM25 Retrieval (Top 15)
          +
Dense Retrieval (Top 15)
          │
          ▼
RRF Fusion (Top 15)
          │
          ▼
Cross Encoder Re-ranking (Top 8)
          │
          ▼
Answer Generation
```

### Release Notes Pipeline

```text
BM25 Retrieval (Top 20)
          │
          ▼
Version Filtering
          │
          ▼
Top 5 Chunks
          │
          ▼
Answer Generation
```

### Mixed Query Pipeline

```text
BM25 Retrieval (Top 15)
          +
Dense Retrieval (Top 15)
          │
          ▼
RRF Fusion (Top 15)
          │
          ▼
Mixed Filtering
          │
          ▼
Top 8 Chunks
          │
          ▼
Answer Generation
```

---

## 🧠 Query Understanding Layer

The query understanding component is responsible for identifying query intent before retrieval begins.

### Intent Classification

Queries are classified into:

* Documentation
* Release Notes
* Mixed

### Version Extraction

Example:

```text
What changed in FastAPI 0.132.0?
```

Extracted Version:

```text
0.132.0
```

### Query Normalization

Queries are normalized to improve retrieval consistency.

### Adaptive Routing

Each query is routed to the most appropriate retrieval pipeline based on its detected intent.

---

## ⚙️ Retrieval Components

### BM25 Retrieval

Sparse lexical retrieval used for exact keyword matching and technical terminology.

### Dense Retrieval

Semantic retrieval using:

```text
BAAI/bge-small-en-v1
```

and FAISS vector search.

### Reciprocal Rank Fusion (RRF)

Combines sparse and dense retrieval rankings into a single candidate ranking.

### Cross-Encoder Re-ranking

Performs pairwise relevance scoring to improve final ranking quality.

---

## 📊 Evaluation Methodology

### Benchmark Dataset

A manually labeled benchmark dataset was created specifically for evaluating retrieval performance.

### Query Distribution

| Query Type    | Count  |
| ------------- | ------ |
| Documentation | 10     |
| Release Notes | 10     |
| Mixed         | 10     |
| **Total**     | **30** |

### Evaluation Metrics

#### Hit Rate@5

Measures whether at least one relevant chunk appears in the retrieved results.

#### Recall@5

Measures how many relevant chunks were successfully retrieved.

#### Mean Reciprocal Rank (MRR)

Measures how highly the first relevant chunk is ranked.

#### Routing Accuracy

Measures the correctness of query routing decisions.

---

## 📈 Experimental Results

### Retrieval Performance

| System                             | Recall@5   | Hit Rate@5 | MRR        |
| ---------------------------------- | ---------- | ---------- | ---------- |
| BM25                               | 0.5867     | 0.8667     | 0.7278     |
| Dense Retrieval                    | 0.5022     | 0.7000     | 0.6150     |
| BM25 + Dense + RRF                 | 0.6478     | 0.9000     | 0.6506     |
| BM25 + Dense + RRF + Cross Encoder | 0.7478     | 0.9667     | 0.8067     |
| ⭐ Final System                     | **0.8467** | **1.0000** | **0.8022** |

### Routing Accuracy

```text
93.33%
28 / 30 Queries Correctly Routed
```

---

## 🔑 Key Findings

### BM25 Remains Strong

BM25 performed exceptionally well on technical documentation due to exact terminology matching.

### Dense Retrieval Alone Was Not Sufficient

Dense retrieval underperformed BM25 when used independently on this corpus.

### RRF Improved Retrieval Robustness

Combining sparse and dense retrieval produced more stable retrieval behavior.

### Cross-Encoder Delivered the Largest Improvement

Cross-Encoder re-ranking significantly improved ranking quality and ranking precision.

### Adaptive Routing Enabled Specialized Retrieval

Different query types benefited from different retrieval strategies rather than a universal retrieval pipeline.

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI

### Retrieval & NLP

* BM25
* FAISS
* Sentence Transformers
* Cross Encoder Models

### LLM

* Groq API
* Llama 3.3 70B

### Frontend

* Next.js
* React
* TypeScript
* Tailwind CSS

### Evaluation

* Custom Benchmark Dataset
* Hit Rate@K
* Recall@K
* MRR
* Routing Accuracy

---

## 📂 Project Structure

```text
Evaluation-Driven-Hybrid-RAG/
│
├── Frontend/
├── backend/
├── retrieval/
├── evaluation/
├── indexing/
├── vector_db/
│
├── rag_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/KottuPrasad/Evaluation-Driven-Hybrid-RAG.git
cd Evaluation-Driven-Hybrid-RAG
```

### Backend Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Start the backend:

```bash
python backend/main.py
```

### Frontend Setup

```bash
cd Frontend
npm install
npm run dev
```

---

## 🔮 Future Improvements

* Expand the benchmark dataset beyond 30 manually labeled queries
* Build automated evaluation dashboards
* Experiment with larger embedding models
* Explore LLM-based query rewriting
* Investigate learning-to-rank retrieval approaches
* Deploy a publicly accessible production version

---

## 👨‍💻 Author

**Prasad Kottu**

Computer Science Student interested in Machine Learning, Information Retrieval, and AI Systems.

GitHub: https://github.com/KottuPrasad

---

## ⭐ Project Highlights

* 1789-Chunk Knowledge Base
* Hybrid Retrieval Architecture
* Cross-Encoder Re-ranking
* Adaptive Query Routing
* Benchmark-Based Evaluation
* Full-Stack Interactive Application
* Evaluation-Driven Development Approach
* End-to-End Retrieval Pipeline
