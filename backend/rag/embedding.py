from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List
import logging

class EmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        try:
            self.model = SentenceTransformer(model_name)
            logging.info(f"Loaded embedding model: {model_name}")
        except Exception as e:
            logging.error(f"Failed to load embedding model {model_name}: {e}")
            # Fallback to a simpler model if the preferred one fails
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            logging.info("Loaded fallback embedding model: all-MiniLM-L6-v2")
    
    def embed_text(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as numpy array
        """
        embedding = self.model.encode(text)
        return embedding
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts: List of input texts to embed
            
        Returns:
            Array of embedding vectors
        """
        embeddings = self.model.encode(texts)
        return embeddings

# Global instance for convenience
embedding_model = EmbeddingModel()