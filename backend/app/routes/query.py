from fastapi import APIRouter, HTTPException

from app.services.retrieval_service import (
    retrieve_documents,
    check_relevance
)

from app.services.llm_service import generate_answer


router = APIRouter()


@router.post("/ask")
async def ask_question(question: str):

    # --------------------------------
    # 1. Validate question
    # --------------------------------

    if not question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )


    # --------------------------------
    # 2. Retrieve documents
    # --------------------------------

    retrieved_documents = retrieve_documents(
        question,
        top_k=5
    )

    print(
        "Retrieved documents:",
        len(retrieved_documents)
    )


    # --------------------------------
    # 3. No documents found
    # --------------------------------

    if not retrieved_documents:

        return {
            "answer": "Insufficient information in the uploaded documents.",
            "sources": []
        }


    # --------------------------------
    # 4. Check relevance
    # --------------------------------

    is_relevant = check_relevance(
        retrieved_documents,
        threshold=0.30
    )

    print(
        "Is relevant:",
        is_relevant
    )


    # --------------------------------
    # 5. Not relevant
    # --------------------------------

    if not is_relevant:

        return {
            "answer": "Insufficient information in the uploaded documents.",
            "sources": []
        }


    # --------------------------------
    # 6. Temporarily bypass reranking
    # --------------------------------

    documents_for_llm = retrieved_documents

    print(
        "Documents sent to LLM:",
        len(documents_for_llm)
    )


    # --------------------------------
    # 7. Generate answer
    # --------------------------------

    try:

        answer = generate_answer(
            question,
            documents_for_llm
        )

    except Exception as error:

        print(
            "LLM ERROR:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=f"LLM generation failed: {str(error)}"
        )


    # --------------------------------
    # 8. Prepare sources
    # --------------------------------

    sources = []

    for document in documents_for_llm:

        metadata = document.get(
            "metadata",
            {}
        )

        sources.append({
            "filename": metadata.get(
                "filename",
                "Unknown"
            ),
            "page": metadata.get(
                "page",
                "Unknown"
            )
        })


    # --------------------------------
    # 9. Return response
    # --------------------------------

    return {
        "answer": answer,
        "sources": sources
    }