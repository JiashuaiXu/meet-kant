from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes_qa import router as qa_router
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Meet-Kant API",
    description="A knowledge system for Kantian philosophy with RAG capabilities",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(qa_router, prefix="/qa", tags=["qa"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Meet-Kant API", "project": "meet-kant"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "meet-kant-api"}