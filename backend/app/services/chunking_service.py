from langchain_text_splitters import RecursiveCharacterTextSplitter


def create_chunks(documents):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=150
    )
    chunks=[]
    for document in documents:

        text_chunks = splitter.split_text(document["text"])

        for index, chunk in enumerate(text_chunks):

            chunks.append({
                "text": chunk,
                "metadata": {
                    "filename": document["metadata"]["filename"],
                    "page": document["metadata"]["page"],
                    "chunk_id": index
                }
            })

    return chunks

