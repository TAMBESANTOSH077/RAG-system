from sentence_transformers import CrossEncoder


reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(question, documents, top_k=3):

    if not documents:
        return []

    pairs = [
        [question, document["text"]]
        for document in documents
    ]

    scores = reranker.predict(pairs)

    for document, score in zip(documents, scores):
        document["rerank_score"] = float(score)

    documents.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return documents[:top_k]