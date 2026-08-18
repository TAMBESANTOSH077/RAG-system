# Multi-Document RAG System

AI-powered document question-answering system built for the StackLab Technologies AI / Software Engineer Technical Assessment.

The system allows users to upload multiple PDF documents and ask questions based only on the information available in those documents.

The main goal is not only to answer questions, but also to **know when NOT to answer**.

---

# 1. Goal

The goal of this project is to build a grounded RAG system that can:

- Accept multiple PDF documents
- Extract and process document content
- Generate embeddings
- Store document vectors
- Perform semantic retrieval
- Check whether retrieved information is relevant
- Use an LLM only when sufficient evidence exists
- Return source references
- Refuse unsupported questions

The key principle is:

> **If sufficient evidence does not exist in the uploaded documents, the system should not answer using the LLM's general knowledge.**

---

# 2. Problem

A normal LLM chatbot can answer questions using its pretrained knowledge.

For example:

```text
User:
Who won the FIFA World Cup in 2022?

LLM:
Argentina won the FIFA World Cup in 2022.


RAG system works

User:
Who won the FIFA World Cup in 2022?

RAG System:
Insufficient information in the uploaded documents.


3. Is there sufficient evidence in the uploaded documents?
                    |
             +------+------+
             |             |
            YES            NO
             |             |
             v             v
        Generate       Do not answer
         Answer




4. Architecture
                         USER
                           |
                           v
                 +-------------------+
                 |     FRONTEND      |
                 |   HTML/CSS/JS     |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 |      FASTAPI      |
                 +---------+---------+
                           |
                +----------+----------+
                |                     |
                v                     v
          PDF Upload              Question
                |                     |
                v                     v
        PDF Text Extraction     Query Embedding
                |                     |
                v                     v
            Chunking            Semantic Search
                |                     |
                v                     v
           Embeddings              ChromaDB
                |                     |
                +----------+----------+
                           |
                           v
                    Retrieved Chunks
                           |
                           v
                       Reranking
                           |
                           v
                   Relevance Check
                      /         \
                     /           \
                  Relevant     Not Relevant
                     |              |
                     v              v
                   Gemini       DO NOT ANSWER
                     |              |
                     v              v
              Answer + Sources   Insufficient
                                Information

5. RAG Pipeline

The complete pipeline is:

                    DOCUMENT INGESTION
                           |
                           v
                      PDF Upload
                           |
                           v
                     PDF Parsing
                           |
                           v
                     Text Extraction
                           |
                           v
                       Chunking
                           |
                           v
                    Embedding Model
                           |
                           v
                       ChromaDB
                           |
                           |
                    USER QUESTION
                           |
                           v
                    Query Embedding
                           |
                           v
                  Semantic Retrieval
                           |
                           v
                      Reranking
                           |
                           v
                  Relevance Checking
                           |
                    +------+------+
                    |             |
                  PASS          FAIL
                    |             |
                    v             v
                  Gemini      Insufficient
                    |         Information
                    v
              Answer + Sources
6. Why I Chose This Architecture

I chose a modular RAG architecture because each stage has a specific responsibility.

PDF Parsing

Converts uploaded PDFs into usable text.

Chunking

Breaks large documents into smaller retrieval units.

Embeddings

Converts text into vectors that represent semantic meaning.

ChromaDB

Stores vectors and document metadata for efficient similarity search.

Semantic Retrieval

Finds document chunks that are semantically related to the question.

Reranking

Improves the ordering of retrieved candidates.

Relevance Checking

Determines whether the retrieved information is sufficient before calling the LLM.

Gemini

Generates the final answer using the retrieved document context.

This separation makes the system easier to debug, test, and improve.

7. Why I Chose the Technologies
Python

Python was selected because it provides a strong ecosystem for:

AI
LLMs
embeddings
vector databases
document processing

I also have prior experience with Python.

FastAPI

FastAPI was selected for the backend because:

It is lightweight
It provides REST APIs
It supports file uploads
It automatically provides Swagger/OpenAPI documentation
It is suitable for AI backend services












