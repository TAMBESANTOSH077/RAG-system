from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from app.services.pdf_service import extract_text_from_pdf
from app.services.chunking_service import create_chunks
from app.services.embedding_service import generate_embeddings
from app.services.vector_service import add_documents


router = APIRouter()


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_pdfs(
    files: list[UploadFile] = File(...)
):

    uploaded_files = []
    total_chunks = 0
    total_vectors = 0

    for file in files:

        if file.content_type != "application/pdf":

            raise HTTPException(
                status_code=400,
                detail=f"{file.filename} is not a PDF file"
            )

        file_path = UPLOAD_DIR / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # 1. Extract text
        documents = extract_text_from_pdf(
            file_path
        )

        # 2. Create chunks
        chunks = create_chunks(
            documents
        )

        # 3. Generate embeddings
        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = generate_embeddings(
            texts
        )

        # 4. Store in ChromaDB
        vectors_added = add_documents(
            chunks,
            embeddings
        )

        total_chunks += len(chunks)
        total_vectors += vectors_added

        uploaded_files.append({
            "filename": file.filename,
            "pages": len(documents),
            "chunks": len(chunks),
            "vectors": vectors_added
        })

    return {
        "message": "PDFs uploaded, embedded and stored successfully",
        "files": uploaded_files,
        "total_chunks": total_chunks,
        "total_vectors": total_vectors
    }