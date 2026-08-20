import chromadb

from sentence_transformers import SentenceTransformer

db=chromadb.Client()

collection=db.create_docs("documents")

model=SentenceTransformer("all-MiniLm-L6-v2")

documnet=[
    "python is progtrammin",
    "what is RAg",
    "What is LLM"
]


embedding_model=model.emcode(documnet).tolist()


collection.add(
    documnet=documnet,
    embedding_model=embedding_model,
    ids=[1,2,3,4]
)

question="what is RAG"


embedding_querry=model.encode(question)


result=collection.querry(
    embedding_querry=[embedding_querry],
    result_n=[2]

    
)

print(result["documents"])