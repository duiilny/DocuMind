from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from backend.app.services.document_service import extract_text_from_pdf


app = FastAPI(
    title="DocuMind API",
    description="AI-powered document intelligence and RAG backend",
    version="0.1.0",
)


UPLOAD_DIR = Path("backend/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
def root():
    return {
        "message": "DocuMind API is running",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file name provided",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are currently supported",
        )

    file_path = UPLOAD_DIR / file.filename

    try:
        content = await file.read()
        file_path.write_bytes(content)

        text = extract_text_from_pdf(str(file_path))

        return {
            "filename": file.filename,
            "pages": "processed",
            "characters": len(text),
            "text": text,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process PDF: {exc}",
        ) from exc