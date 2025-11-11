"""
Script to bootstrap the Kant knowledge system:
1. Load graph data into Neo4j
2. Create vector store from text data
"""

import os
import sys
from pathlib import Path

# Add the backend directory to the path so we can import modules
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from backend.graph.neo4j_loader import load_all_data
from backend.rag.retriever import Retriever

def main():
    print("🤖 Starting Meet-Kant data bootstrap process...")
    
    # Step 1: Load graph data into Neo4j
    print("\n1. Loading graph data into Neo4j...")
    try:
        load_all_data()
        print("✅ Graph data loaded successfully")
    except Exception as e:
        print(f"❌ Error loading graph data: {e}")
        print("Make sure Neo4j is running and credentials are correct in .env file")
        return 1
    
    # Step 2: Create vector store from text data
    print("\n2. Creating vector store from text data...")
    try:
        # Create a retriever instance which will build the index if it doesn't exist
        retriever = Retriever()
        print("✅ Vector store created successfully")
    except Exception as e:
        print(f"❌ Error creating vector store: {e}")
        return 1
    
    print("\n🎉 Bootstrap process completed successfully!")
    print("\nTo start the API server:")
    print("1. cd backend")
    print("2. uvicorn app:app --reload --port 8000")
    print("\nTo access the frontend:")
    print("1. Open frontend/index.html in your browser")
    print("2. Or use a local server like: python -m http.server 8080 in the frontend directory")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())