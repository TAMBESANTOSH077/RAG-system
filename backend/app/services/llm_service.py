import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_answer(question: str, documents: list):

    context_parts = []

    for document in documents:

        context_parts.append(
            f"""
Source: {document['metadata']['filename']}
Page: {document['metadata']['page']}

Content:
{document['text']}
"""
        )

    context = "\n\n".join(context_parts)

    prompt = f"""
You are a document question-answering assistant.

Answer the user's question ONLY using the provided document context.

Do not use your general knowledge.

If the provided context does not contain enough information
to answer the question, say exactly:

"Insufficient information in the uploaded documents."

Question:
{question}

Document Context:
{context}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text