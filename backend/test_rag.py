import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.rag.medical_rag import get_medical_rag
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_medical_knowledge():
    
    logger.info("="*60)
    logger.info("STEP 1: Loading Medical Knowledge")
    logger.info("="*60)
    
    rag = get_medical_rag()
    
    result = rag.load_knowledge(reset=False)
    
    logger.info(f"Load result: {result}")
    logger.info("")
    
    return rag


def test_search(rag):
    
    logger.info("="*60)
    logger.info("STEP 2: Testing Semantic Search")
    logger.info("="*60)
    
    test_queries = [
        "I have fever and cough",
        "My head hurts really bad",
        "I feel dizzy and nauseous",
        "Chest pain and shortness of breath",
        "What is influenza?"
    ]
    
    for query in test_queries:
        logger.info(f"\n{'='*60}")
        logger.info(f"Query: '{query}'")
        logger.info(f"{'='*60}")
        
        results = rag.search(query, n_results=3)
        
        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            similarity = result['similarity']
            text_preview = result['text'][:150].replace('\n', ' ')
            
            logger.info(f"\n{i}. {metadata['name']} ({metadata['type']})")
            logger.info(f"   Similarity: {similarity:.3f} ({similarity*100:.1f}%)")
            logger.info(f"   Preview: {text_preview}...")
        
        logger.info("")


def test_filtered_search(rag):
    
    logger.info("="*60)
    logger.info("STEP 3: Testing Filtered Search")
    logger.info("="*60)
    
    logger.info("\nSearching SYMPTOMS only for: 'I feel hot and tired'")
    results = rag.search_symptoms("I feel hot and tired", n_results=3)
    
    for i, result in enumerate(results, 1):
        logger.info(f"{i}. {result['metadata']['name']} - {result['similarity']:.3f}")
    
    logger.info("\nSearching DISEASES only for: 'respiratory infection'")
    results = rag.search_diseases("respiratory infection", n_results=3)
    
    for i, result in enumerate(results, 1):
        logger.info(f"{i}. {result['metadata']['name']} - {result['similarity']:.3f}")
    
    logger.info("")


def display_statistics(rag):
    
    logger.info("="*60)
    logger.info("STEP 4: Database Statistics")
    logger.info("="*60)
    
    total_docs = rag.vector_store.get_document_count()
    embedding_dim = rag.embedding_model.get_dimension()
    
    logger.info(f"Total documents in database: {total_docs}")
    logger.info(f"Embedding dimension: {embedding_dim}")
    logger.info(f"Storage location: {rag.vector_store.persist_directory}")
    logger.info("")


def main():
    
    try:
        logger.info("\n" + "="*60)
        logger.info("MEDICAL RAG SYSTEM TEST")
        logger.info("="*60 + "\n")
        
        rag = load_medical_knowledge()
        
        test_search(rag)
        
        test_filtered_search(rag)
        
        display_statistics(rag)
        
        logger.info("="*60)
        logger.info("✅ ALL TESTS PASSED!")
        logger.info("="*60)
        logger.info("\nRAG system is ready to use.")
        logger.info("I can now integrate it with FastAPI endpoints.")
        
    except Exception as e:
        logger.error(f"❌ TEST FAILED: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()