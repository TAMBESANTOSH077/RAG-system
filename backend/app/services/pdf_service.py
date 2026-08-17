from pathlib import Path
from pypdf import PdfReader


def extract_text_from_pdf(file_path: Path):
    documents = []

    reader = PdfReader(file_path)

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text and text.strip():
            documents.append({
                "text": text.strip(),
                "metadata": {
                    "filename": file_path.name,
                    "page": page_number
                }
            })

    return documents