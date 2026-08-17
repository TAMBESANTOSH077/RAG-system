import chromadb


client = chromadb.PersistentClient(
    path="chroma_db"
)


collection = client.get_or_create_collection(
    name="documents"
)


def add_documents(chunks, embeddings):

    ids = []

    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        chunk_id = (
            f"{chunk['metadata']['filename']}"
            f"_{chunk['metadata']['page']}"
            f"_{chunk['metadata']['chunk_id']}"
            f"_{index}"
        )

        ids.append(chunk_id)

        documents.append(
            chunk["text"]
        )

        metadatas.append(
            chunk["metadata"]
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )

    return len(ids)