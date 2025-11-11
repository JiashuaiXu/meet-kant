from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from backend.rag.retriever import Retriever
from backend.rag.prompt_templates import QA_PROMPT
import logging

router = APIRouter()

# Request and response models
class QARequest(BaseModel):
    question: str
    lang: str = "zh"  # Default to Chinese

class Evidence(BaseModel):
    work_id: str
    para_id: str
    lang: str
    text: str
    score: float

class GraphHit(BaseModel):
    entity_id: str
    entity_type: str
    name: str
    relationship: str

class QAResponse(BaseModel):
    answer: str
    evidence: List[Evidence]
    graph_hits: List[GraphHit]

# Initialize retriever
try:
    retriever = Retriever()
except Exception as e:
    logging.error(f"Failed to initialize retriever: {e}")
    retriever = None

@router.post("/rag", response_model=QAResponse)
async def qa_rag(request: QARequest):
    if not retriever:
        raise HTTPException(status_code=500, detail="Retriever not initialized")
    
    try:
        # Retrieve relevant documents
        relevant_docs = retriever.retrieve(request.question, lang=request.lang)
        
        # Format evidence for prompt
        evidence_blocks = []
        for doc in relevant_docs:
            evidence_blocks.append(f"Work ID: {doc['work_id']}, Para ID: {doc['para_id']}, Lang: {doc['lang']}\nText: {doc['text']}")
        
        evidence_str = "\n\n".join(evidence_blocks)
        
        # Format the prompt
        prompt = QA_PROMPT.format(
            question=request.question,
            evidence_blocks=evidence_str
        )
        
        # For now, return a mock answer with evidence
        # In a real implementation, you would call an LLM here
        answer = f"Based on the retrieved evidence, here's an answer to your question: '{request.question}'. This is a placeholder response that would normally come from an LLM based on the provided evidence."
        
        # Format evidence for response
        formatted_evidence = []
        for doc in relevant_docs:
            formatted_evidence.append(Evidence(
                work_id=doc['work_id'],
                para_id=doc['para_id'],
                lang=doc['lang'],
                text=doc['text'][:200] + "..." if len(doc['text']) > 200 else doc['text'],  # Truncate long texts
                score=doc.get('score', 0.0)
            ))
        
        # Mock graph hits (in a real system, this would come from graph queries)
        graph_hits = [
            GraphHit(
                entity_id="kant",
                entity_type="Person",
                name="Immanuel Kant",
                relationship="author"
            )
        ]
        
        return QAResponse(
            answer=answer,
            evidence=formatted_evidence,
            graph_hits=graph_hits
        )
    except Exception as e:
        logging.error(f"Error in QA RAG: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing QA request: {str(e)}")

@router.get("/graph/neighbor")
async def get_graph_neighbor(entity_id: str, k: int = 3):
    # This would connect to Neo4j and get neighbors
    # For now, return mock data
    neighbors = [
        {
            "entity_id": "categorical_imperative",
            "entity_type": "Concept",
            "name": "Categorical Imperative",
            "relationship": "defined_by"
        },
        {
            "entity_id": "pure_reason",
            "entity_type": "Work", 
            "name": "Critique of Pure Reason",
            "relationship": "authored"
        }
    ]
    return {"entity_id": entity_id, "neighbors": neighbors[:k]}