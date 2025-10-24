from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        logger.info(f"Loading embedding model: {model_name}")
        
        try:
            self.model = SentenceTransformer(model_name)
            
            self.dimension = self.model.get_sentence_embedding_dimension()
            
            logger.info(f"Model loaded successfully. Embedding dimension: {self.dimension}")
            
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise
    
    
    def encode(self, texts: Union[str, List[str]], batch_size: int = 32) -> np.ndarray:
        
        try:
            if isinstance(texts, str):
                texts = [texts]
                return_single = True
            else:
                return_single = False
            
            logger.info(f"Encoding {len(texts)} text(s)")
            
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                normalize_embeddings=True,
                show_progress_bar=False,
                convert_to_numpy=True
            )
            
            if return_single:
                return embeddings[0]
            
            return embeddings
            
        except Exception as e:
            logger.error(f"Failed to encode texts: {e}")
            raise
    
    
    def encode_batch(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        
        return self.encode(texts, batch_size=batch_size)
    
    
    def similarity(self, text1: str, text2: str) -> float:

        try:
            
            emb1 = self.encode(text1)
            emb2 = self.encode(text2)
            
            similarity_score = np.dot(emb1, emb2)
            
            return float(similarity_score)
            
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            raise
    
    
    def get_dimension(self) -> int:

        return self.dimension


_embedding_model = None


def get_embedding_model() -> EmbeddingModel:
    
    global _embedding_model
    
    if _embedding_model is None:
        logger.info("Creating global embedding model instance")
        _embedding_model = EmbeddingModel()
    
    return _embedding_model