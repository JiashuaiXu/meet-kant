import json
import faiss
import numpy as np
from typing import List, Dict, Any
from backend.rag.embedding import embedding_model
import logging
import os

class Retriever:
    def __init__(self, vector_store_path: str = "resource/kant/vector_store.index", 
                 texts_path: str = "resource/kant/texts/"):
        """
        Initialize the retriever with vector store and text data.
        
        Args:
            vector_store_path: Path to the FAISS vector store
            texts_path: Path to the directory containing text files
        """
        self.vector_store_path = vector_store_path
        self.texts_path = texts_path
        self.index = None
        self.texts_data = []
        
        # Load text data from JSONL files
        self._load_texts()
        
        # Build or load the vector index
        if os.path.exists(vector_store_path):
            self._load_index()
        else:
            self._build_index()
    
    def _load_texts(self):
        """Load text data from JSONL files in the texts directory."""
        import glob
        
        text_files = glob.glob(os.path.join(self.texts_path, "*.jsonl"))
        
        if not text_files:
            # If no files found, create sample data
            logging.info("No text files found, creating sample data")
            self._create_sample_texts()
        else:
            for file_path in text_files:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            self.texts_data.append({
                                'work_id': data.get('work_id', ''),
                                'para_id': data.get('para_id', ''),
                                'lang': data.get('lang', 'unknown'),
                                'text': data.get('text', ''),
                                'original': data  # Store original data for potential metadata
                            })
                        except json.JSONDecodeError:
                            logging.warning(f"Skipping invalid JSON line in {file_path}")
    
    def _create_sample_texts(self):
        """Create sample text data for demonstration purposes."""
        sample_texts = [
            {
                "work_id": "pure_reason",
                "para_id": "1",
                "lang": "en",
                "text": "The Critique of Pure Reason is Kant's major work in which he attempts to determine the limits and scope of metaphysics. He argues that while knowledge begins with experience, it does not all arise out of experience."
            },
            {
                "work_id": "pure_reason",
                "para_id": "2", 
                "lang": "en",
                "text": "Kant introduces the concept of the categorical imperative as a fundamental principle of morality. It is a command that applies to all rational beings regardless of their desires or inclinations."
            },
            {
                "work_id": "pure_reason",
                "para_id": "3",
                "lang": "zh",
                "text": "《纯粹理性批判》是康德的主要著作，在书中他试图确定形而上学的界限和范围。他论证说，虽然知识始于经验，但并非全部源于经验。"
            },
            {
                "work_id": "pure_reason", 
                "para_id": "4",
                "lang": "zh",
                "text": "康德引入了定言令式的概念，作为道德的根本原则。这是一种适用于所有理性存在的命令，不管他们的欲望或倾向如何。"
            },
            {
                "work_id": "pure_reason",
                "para_id": "5",
                "lang": "de",
                "text": "Die Kritik der reinen Vernunft ist das Hauptwerk Kants, in dem er zu bestimmen sucht, was Metaphysik sein kann. Er argumentiert, dass zwar alles Wissen mit der Erfahrung anfängt, aber nicht alles Wissen aus der Erfahrung entspringt."
            },
            {
                "work_id": "practical_reason",
                "para_id": "1",
                "lang": "en", 
                "text": "The Critique of Practical Reason focuses on the foundations of moral action. Kant argues that moral law is given by rational beings to themselves through the categorical imperative."
            },
            {
                "work_id": "practical_reason",
                "para_id": "2",
                "lang": "en",
                "text": "Kant distinguishes between phenomenon and noumenon. The phenomenon is the world as we experience it, while the noumenon is the world of things-in-themselves, which we cannot directly know."
            }
        ]
        
        for data in sample_texts:
            self.texts_data.append({
                'work_id': data['work_id'],
                'para_id': data['para_id'],
                'lang': data['lang'],
                'text': data['text'],
                'original': data
            })
    
    def _build_index(self):
        """Build the FAISS vector index from text data."""
        if not self.texts_data:
            logging.warning("No texts to build index from")
            return
        
        # Extract texts for embedding
        texts = [item['text'] for item in self.texts_data]
        
        # Generate embeddings
        logging.info(f"Generating embeddings for {len(texts)} texts...")
        embeddings = embedding_model.embed_texts(texts)
        
        # Convert to float32 for FAISS
        embeddings = embeddings.astype('float32')
        
        # Build FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)  # Inner product (cosine similarity)
        
        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)
        
        # Add embeddings to index
        self.index.add(embeddings)
        
        # Save the index
        faiss.write_index(self.index, self.vector_store_path)
        logging.info(f"Built and saved FAISS index with {len(texts)} vectors")
    
    def _load_index(self):
        """Load the pre-built FAISS vector index."""
        self.index = faiss.read_index(self.vector_store_path)
        logging.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
    
    def retrieve(self, query: str, top_k: int = 5, lang: str = None) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: Input query text
            top_k: Number of top results to return
            lang: Language filter (optional)
            
        Returns:
            List of relevant documents with metadata
        """
        if self.index is None or len(self.texts_data) == 0:
            logging.warning("Index or texts data not available")
            return []
        
        # Generate embedding for query
        query_embedding = embedding_model.embed_text(query)
        query_embedding = np.array([query_embedding.astype('float32')])
        
        # Normalize query embedding
        faiss.normalize_L2(query_embedding)
        
        # Perform similarity search
        scores, indices = self.index.search(query_embedding, min(top_k * 3, len(self.texts_data)))  # Get more results than needed for filtering
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts_data):
                text_data = self.texts_data[idx]
                
                # Apply language filter if specified
                if lang and text_data['lang'] != lang:
                    continue
                
                result = {
                    'work_id': text_data['work_id'],
                    'para_id': text_data['para_id'], 
                    'lang': text_data['lang'],
                    'text': text_data['text'],
                    'score': float(scores[0][i])
                }
                results.append(result)
        
        # Return top_k results after filtering
        return results[:top_k]


# Example usage
if __name__ == "__main__":
    retriever = Retriever()
    
    # Test retrieval
    results = retriever.retrieve("What is the categorical imperative?", lang="en")
    
    for i, result in enumerate(results):
        print(f"Result {i+1}:")
        print(f"  Work ID: {result['work_id']}")
        print(f"  Para ID: {result['para_id']}")
        print(f"  Lang: {result['lang']}")
        print(f"  Score: {result['score']:.4f}")
        print(f"  Text: {result['text'][:100]}...")
        print()