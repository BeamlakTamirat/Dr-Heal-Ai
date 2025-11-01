from typing import Dict, Any
import logging

from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class SymptomAnalyzerAgent(BaseAgent):
    
    def __init__(self):
        super().__init__(
            name="SymptomAnalyzer",
            role="Analyzes user symptoms and assesses severity"
        )
        
        self.prompt_template = """You are a medical symptom analyzer. Analyze the user's symptoms carefully.

CONTEXT FROM MEDICAL KNOWLEDGE BASE:
{context}

USER'S SYMPTOMS:
{query}

Provide a structured analysis:

1. **IDENTIFIED SYMPTOMS:**
   - List each symptom mentioned
   - Note duration and severity if mentioned

2. **SEVERITY ASSESSMENT:**
   - Overall severity: Mild / Moderate / Severe
   - Justification for the assessment

3. **POSSIBLE CONDITIONS:**
   - Based on the context, list 2-3 most likely conditions
   - Explain why each is possible

4. **IMMEDIATE RECOMMENDATIONS:**
   - What the person should do now
   - Self-care measures
   - When to seek medical attention

5. **RED FLAGS:**
   - Any emergency warning signs present?
   - If yes, emphasize urgency

Be empathetic, clear, and thorough. Focus on safety."""
    
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(state, dict):
            query = state['query']
        else:
            query = state.query
        
        logger.info(f"[{self.name}] Processing query: {query}")
        
        rag_results = self.retrieve_knowledge(
            query=query,
            n_results=5
        )
        
        context = self.format_context(rag_results)
        
        prompt = self.prompt_template.format(
            context=context,
            query=query
        )
        
        analysis = self.generate_response(prompt)
        
        if isinstance(state, dict):
            state['rag_results'] = rag_results
            state['agent_outputs']['symptom_analysis'] = analysis
            state['metadata']['symptoms_retrieved'] = len(rag_results)
        else:
            state.rag_results = rag_results
            state.agent_outputs['symptom_analysis'] = analysis
            state.metadata['symptoms_retrieved'] = len(rag_results)
        
        logger.info(f"[{self.name}] Analysis complete (length: {len(analysis)})")
        
        return state