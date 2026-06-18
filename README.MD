# 🚀 Evaluation-Driven Hybrid RAG System

### Hybrid Retrieval-Augmented Generation with BM25, Dense Retrieval, RRF Fusion, Cross-Encoder Re-ranking, and Adaptive Query Routing

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python\&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.137-009688?logo=fastapi\&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange)
![BM25](https://img.shields.io/badge/BM25-Sparse_Retrieval-green)
![Cross Encoder](https://img.shields.io/badge/Cross--Encoder-Re--Ranking-purple)
![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js)
![Routing Accuracy](https://img.shields.io/badge/Routing_Accuracy-93.33%25-success)

---

## 📖 Overview

This project presents an **Evaluation-Driven Hybrid Retrieval-Augmented Generation (RAG) System** designed for answering questions over **FastAPI Documentation** and **FastAPI Release Notes**.

Unlike traditional RAG systems that rely on a single retrieval strategy, this system combines:

* BM25 Sparse Retrieval
* Dense Vector Retrieval
* Reciprocal Rank Fusion (RRF)
* Cross-Encoder Re-ranking
* Query Understanding
* Adaptive Retrieval Routing

The project was developed using an **evaluation-first methodology**, where retrieval improvements were validated through a manually labeled benchmark dataset and quantitative metrics.

---

## 🎯 Problem Statement

Most RAG systems process every query using the same retrieval pipeline regardless of query intent.

However, different query categories require different retrieval behavior:

* Documentation questions require semantic understanding of APIs and concepts.
* Release note questions require version-aware retrieval.
* Mixed questions require combining documentation knowledge with version-specific information.

This project investigates whether retrieval quality can be improved through:

* Hybrid Retrieval
* Re-ranking
* Query Understanding
* Adaptive Routing
* Evaluation-Driven Optimization

---

## 🔬 Research Questions

This project explores the following questions:

1. Can sparse and dense retrieval be combined to improve retrieval quality?
2. Does Reciprocal Rank Fusion improve retrieval robustness?
3. How much improvement can Cross-Encoder re-ranking provide?
4. Can query understanding improve retrieval effectiveness?
5. Does adaptive routing outperform a universal retrieval pipeline?

---

## 📚 Dataset

### Knowledge Sources

The retrieval corpus consists of:

* FastAPI Documentation
* FastAPI Release Notes

### Corpus Statistics

| Source        | Chunks |
| ------------- | ------ |
| Documentation | 1112   |
| Release Notes | 677    |
| Total         | 1789   |

---

## 🏗️ System Architecture

> Replace the image below with your architecture diagram.

![System Architecture](images/architecture.png)

### High-Level Flow

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
 ┌────┼────┐
 │    │    │
 ▼    ▼    ▼
Documentation
Release Notes
Mixed
      │
      ▼
Specialized Retrieval Pipeline
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
Response Generation
```

---

### Release Notes Pipeline

```text
BM25 Retrieval (Top 20)
          │
          ▼
Version-Aware Filtering
          │
          ▼
Top 5 Chunks
          │
          ▼
Response Generation
```

---

### Mixed Pipeline

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
Response Generation
```

---

## 🧠 Query Understanding Layer

The system includes a dedicated query understanding module responsible for:

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

User queries are normalized before retrieval to improve search quality.

### Adaptive Routing

Queries are routed to the most appropriate retrieval pipeline based on detected intent.

---

## ⚙️ Retrieval Components

### BM25 Retrieval

Sparse retrieval used for exact keyword matching and technical terminology.

### Dense Retrieval

Semantic retrieval using:

```text
BAAI/bge-small-en-v1
```

and FAISS vector search.

### Reciprocal Rank Fusion (RRF)

Combines sparse and dense retrieval rankings into a unified candidate list.

### Cross-Encoder Re-ranking

Performs pairwise relevance scoring to improve ranking quality.

---

## 📊 Evaluation Methodology

### Benchmark Dataset

A manually labeled benchmark dataset was created specifically for evaluating retrieval performance.

### Query Distribution

| Query Type    | Count |
| ------------- | ----- |
| Documentation | 10    |
| Release Notes | 10    |
| Mixed         | 10    |
| Total         | 30    |

### Metrics

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

BM25 performed surprisingly well on technical documentation due to exact terminology matching.

### Dense Retrieval Alone Was Not Sufficient

Dense retrieval underperformed BM25 when used independently.

### RRF Improved Retrieval Robustness

Combining sparse and dense retrieval produced more stable retrieval behavior.

### Cross-Encoder Produced the Largest Gain

Cross-Encoder re-ranking delivered the largest improvement in retrieval quality.

### Query Understanding Improved Retrieval

Adaptive routing enabled specialized retrieval strategies for different query categories.

---

## 🛠️ Technology Stack

### Backend

* Python
* FastAPI

### Retrieval

* BM25
* FAISS
* Sentence Transformers
* Cross Encoder

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

---

## 📂 Project Structure

```text
Project1/
│
├── frontend/
├── backend/
├── chunking/
├── ingestion/
├── retrieval/
├── evaluation/
├── indexing/
├── llm/
├── config/
├── vector_db/
│
├── rag_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Running Locally

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Evaluation-Driven-Hybrid-RAG.git
cd Evaluation-Driven-Hybrid-RAG
```

### Backend Setup

```bash
pip install -r requirements.txt
python backend/main.py
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

## 🔮 Future Work

Potential future improvements include:

* Larger benchmark datasets
* Query rewriting
* Metadata-aware retrieval
* Learning-to-rank models
* Automated evaluation pipelines
* Advanced hybrid scoring strategies

---

## 📬 Contact

**Prasad Kottu**

For questions, suggestions, or collaboration opportunities, feel free to connect through GitHub.

---

## ⭐ Project Highlights

* Evaluation-Driven Development
* 1789-Chunk Knowledge Base
* Hybrid Retrieval Architecture
* Cross-Encoder Re-ranking
* Adaptive Query Routing
* Benchmark-Based Evaluation
* Full-Stack Interactive Demo
