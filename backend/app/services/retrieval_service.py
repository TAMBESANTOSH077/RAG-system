from app.services.vector_service import collection
from app.services.embedding_service import generate_embeddings


def retrieve_documents(question: str, top_k: int = 5):

    # Generate embedding for the user's question
    query_embedding = generate_embeddings(
        [question]
    )[0]

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[
            query_embedding.tolist()
        ],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    retrieved_documents = []

    # No results
    if not results.get("documents"):
        return []

    if not results["documents"][0]:
        return []

    # Process retrieved chunks
    for i in range(len(results["documents"][0])):

        document = results["documents"][0][i]
        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        # Convert distance to a simple similarity score
        similarity = 1 / (1 + distance)

        retrieved_documents.append({
            "text": document,
            "metadata": metadata,
            "distance": distance,
            "similarity": similarity
        })

    # Debug information
    print("\n==============================")
    print("QUESTION:", question)
    print("RETRIEVED DOCUMENTS:", len(retrieved_documents))

    for index, result in enumerate(retrieved_documents):

        print(f"\n--- RESULT {index + 1} ---")
        print("Similarity:", result["similarity"])
        print("Metadata:", result["metadata"])
        print("Text:", result["text"][:500])

    print("==============================\n")

    return retrieved_documents


def check_relevance(
    results,
    threshold=0.40
):

    if not results:
        return False

    best_similarity = max(
        result["similarity"]
        for result in results
    )

    print(
        "Best similarity:",
        round(best_similarity, 4)
    )

    return best_similarity >= threshold