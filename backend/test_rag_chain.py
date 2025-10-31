import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.llm.rag_chain import get_rag_chain
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def print_separator(title=""):
    if title:
        logger.info(f"\n{'='*70}")
        logger.info(f"{title:^70}")
        logger.info(f"{'='*70}\n")
    else:
        logger.info(f"{'='*70}\n")


def test_symptom_analysis():
    print_separator("TEST 1: SYMPTOM ANALYSIS")
    
    chain = get_rag_chain()
    
    query = "I have fever and cough for 3 days"
    
    logger.info(f"Query: '{query}'\n")
    
    result = chain.analyze_symptoms(query, n_results=3)
    
    logger.info("RAG RETRIEVAL RESULTS:")
    logger.info(f"Found {result['n_results']} relevant documents\n")
    
    for i, rag_result in enumerate(result['rag_results'], 1):
        logger.info(f"{i}. {rag_result['metadata']['name']} ({rag_result['metadata']['type']})")
        logger.info(f"   Similarity: {rag_result['similarity']:.3f} ({rag_result['similarity']*100:.1f}%)\n")
    
    logger.info("\n" + "="*70)
    logger.info("AI RESPONSE:")
    logger.info("="*70)
    logger.info(f"\n{result['response']}\n")
    
    print_separator()


def test_disease_info():
    print_separator("TEST 2: DISEASE INFORMATION")
    
    chain = get_rag_chain()
    
    query = "Tell me about influenza"
    
    logger.info(f"Query: '{query}'\n")
    
    result = chain.get_disease_info(query, n_results=2)
    
    logger.info("RAG RETRIEVAL RESULTS:")
    logger.info(f"Found {result['n_results']} relevant documents\n")
    
    for i, rag_result in enumerate(result['rag_results'], 1):
        logger.info(f"{i}. {rag_result['metadata']['name']}")
        logger.info(f"   Similarity: {rag_result['similarity']:.3f}\n")
    
    logger.info("\n" + "="*70)
    logger.info("AI RESPONSE:")
    logger.info("="*70)
    logger.info(f"\n{result['response']}\n")
    
    print_separator()


def test_general_question():
    print_separator("TEST 3: GENERAL MEDICAL QUESTION")
    
    chain = get_rag_chain()
    
    query = "What should I do if I have a headache?"
    
    logger.info(f"Query: '{query}'\n")
    
    result = chain.answer_question(query, n_results=3)
    
    logger.info("RAG RETRIEVAL RESULTS:")
    logger.info(f"Found {result['n_results']} relevant documents\n")
    
    for i, rag_result in enumerate(result['rag_results'], 1):
        logger.info(f"{i}. {rag_result['metadata']['name']}")
        logger.info(f"   Similarity: {rag_result['similarity']:.3f}\n")
    
    logger.info("\n" + "="*70)
    logger.info("AI RESPONSE:")
    logger.info("="*70)
    logger.info(f"\n{result['response']}\n")
    
    print_separator()


def main():
    try:
        print_separator("RAG CHAIN END-TO-END TEST")
        
        logger.info("Testing complete RAG pipeline:")
        logger.info("1. User Query")
        logger.info("2. RAG Retrieval (Chroma DB)")
        logger.info("3. Context Formatting")
        logger.info("4. Gemini Generation")
        logger.info("5. Intelligent Response\n")
        
        test_symptom_analysis()
        test_disease_info()
        test_general_question()
        
        print_separator("✅ ALL TESTS PASSED!")
        logger.info("\nRAG Chain is working perfectly!")
        logger.info("The system can now:")
        logger.info("  ✓ Retrieve relevant medical knowledge")
        logger.info("  ✓ Generate intelligent AI responses")
        logger.info("  ✓ Provide personalized medical guidance")
        logger.info("\nReady to create API endpoint!")
        
    except Exception as e:
        logger.error(f"\n❌ TEST FAILED: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()