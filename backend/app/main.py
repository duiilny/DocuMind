from fastapi import FastAPI

app = FastAPI(
    title="DocuMind API",
    description="AI-powered document intelligence and RAG backend",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "DocuMind API is running",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}