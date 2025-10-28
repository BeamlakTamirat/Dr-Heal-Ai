import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import logging
import os

from app.rag.embeddings import get_embedding_model

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MedicalVectorStore:
    
    def __init__(
        self,
        collection_name: str = "medical_knowledge",
        persist_directory: str = "./chroma_db"
    ):
       
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        
        self.embedding_model = get_embedding_model()
        
        logger.info(f"Initializing Chroma DB at {persist_directory}")
        
        try:
            os.makedirs(persist_directory, exist_ok=True)
            
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False
                )
            )
            
            self.collection = self.client.get_or_create_collection(
                name=collection_name,
                metadata={"description": "Medical knowledge base for Dr.Heal AI"}
            )
            
            logger.info(f"Collection '{collection_name}' ready. Documents: {self.collection.count()}")
            
        except Exception as e:
            logger.error(f"Failed to initialize vector store: {e}")
            raise
    
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict]] = None,
        ids: Optional[List[str]] = None
    ) -> None:
        
        try:
            if ids is None:
                ids = [f"doc_{i}" for i in range(len(texts))]
            
            if metadatas is None:
                metadatas = [{} for _ in range(len(texts))]
            
            logger.info(f"Adding {len(texts)} documents to collection")
            
            embeddings = self.embedding_model.encode_batch(texts)
            
            embeddings_list = embeddings.tolist()
            
            self.collection.upsert(
                ids=ids,
                embeddings=embeddings_list,
                documents=texts,
                metadatas=metadatas
            )

            
            logger.info(f"Successfully added {len(texts)} documents")
            
        except Exception as e:
            logger.error(f"Failed to add documents: {e}")
            raise
    
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        filter_metadata: Optional[Dict] = None
    ) -> Dict:
        
        try:
            logger.info(f"Searching for: '{query}' (n_results={n_results})")
            
            query_embedding = self.embedding_model.encode(query)
            
            query_embedding_list = query_embedding.tolist()
            
            results = self.collection.query(
                query_embeddings=[query_embedding_list],
                n_results=n_results,
                where=filter_metadata,
                include=["documents", "metadatas", "distances"]
            )
            
            logger.info(f"Found {len(results['documents'][0])} results")
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to search: {e}")
            raise
    
    
    def get_document_count(self) -> int:
        
        return self.collection.count()
    
    
    def delete_collection(self) -> None:
        
        try:
            logger.warning(f"Deleting collection '{self.collection_name}'")
            self.client.delete_collection(name=self.collection_name)
            logger.info("Collection deleted successfully")
            
        except Exception as e:
            logger.error(f"Failed to delete collection: {e}")
            raise
    
    
    def reset(self) -> None:
        
        try:
            logger.info("Resetting collection")
            self.delete_collection()
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Medical knowledge base for Dr.Heal AI"}
            )
            
            logger.info("Collection reset successfully")
            
        except Exception as e:
            logger.error(f"Failed to reset collection: {e}")
            raise



_vector_store = None


def get_vector_store() -> MedicalVectorStore:

    global _vector_store
    
    if _vector_store is None:
        logger.info("Creating global vector store instance")
        _vector_store = MedicalVectorStore()
    
    return _vector_store