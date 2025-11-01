from typing import Dict, Any
import logging

from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class DiseaseExpertAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DiseaseExpert",
            role="Provides comprehensive disease information"
        )
        
        self.prompt_template = """You are a medical disease expert. Provide comprehensive information about the condition.

CONTEXT FROM MEDICAL KNOWLEDGE BASE:
{context}

USER'S QUESTION:
{query}

Provide detailed information:

1. **DISEASE OVERVIEW:**
   - What is this condition?
   - How common is it?
   - Who is most affected?

2. **SYMPTOMS:**
   - Common symptoms
   - Early warning signs
   - How symptoms progress

3. **CAUSES & RISK FACTORS:**
   - What causes this condition?
   - Who is at higher risk?
   - Contributing factors

4. **DIAGNOSIS:**
   - How is it diagnosed?
   - What tests are used?

5. **TREATMENT OPTIONS:**
   - Medical treatments
   - Self-care measures
   - Expected recovery time

6. **PREVENTION:**
   - How to prevent this condition
   - Lifestyle modifications
   - Vaccines or preventive measures

7. **COMPLICATIONS:**
   - Possible complications if untreated
   - When to see a doctor

Be thorough, educational, and reassuring. Use simple language."""
    
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(state, dict):
            query = state['query']
        else:
            query = state.query
        
        logger.info(f"[{self.name}] Processing query: {query}")
        
        rag_results = self.retrieve_knowledge(
            query=query,
            n_results=3,
            filter_type="disease"
        )
        
        context = self.format_context(rag_results)
        
        prompt = self.prompt_template.format(
            context=context,
            query=query
        )
        
        disease_info = self.generate_response(prompt)
        
        if isinstance(state, dict):
            state['rag_results'] = rag_results
            state['agent_outputs']['disease_info'] = disease_info
            state['metadata']['diseases_retrieved'] = len(rag_results)
        else:
            state.rag_results = rag_results
            state.agent_outputs['disease_info'] = disease_info
            state.metadata['diseases_retrieved'] = len(rag_results)
        
        logger.info(f"[{self.name}] Disease info complete (length: {len(disease_info)})")
        
        return state