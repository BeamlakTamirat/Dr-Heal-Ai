from typing import Dict, Any
import logging

from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class TreatmentAdvisorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TreatmentAdvisor",
            role="Recommends evidence-based treatments"
        )
        
        self.prompt_template = """You are a medical treatment advisor. Provide practical treatment recommendations.

CONTEXT FROM MEDICAL KNOWLEDGE BASE:
{context}

USER'S SITUATION:
{query}

Provide actionable treatment advice:

1. **IMMEDIATE SELF-CARE:**
   - What can be done at home right now?
   - Rest, hydration, comfort measures
   - Specific actions for symptom relief

2. **OVER-THE-COUNTER MEDICATIONS:**
   - Recommended OTC medications
   - Proper dosages (general guidelines)
   - Precautions and contraindications
   - When NOT to use certain medications

3. **HOME REMEDIES:**
   - Natural remedies that may help
   - Dietary recommendations
   - Activity modifications

4. **LIFESTYLE ADJUSTMENTS:**
   - Changes to daily routine
   - Sleep recommendations
   - Stress management

5. **WHEN TO SEE A DOCTOR:**
   - Clear criteria for medical consultation
   - What symptoms indicate worsening
   - How urgent is medical attention?

6. **WHAT TO EXPECT:**
   - Typical recovery timeline
   - Signs of improvement
   - Follow-up care

Be practical, safe, and clear. Always prioritize safety and professional medical care when needed."""
    
    
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
        
        treatment_advice = self.generate_response(prompt)
        
        if isinstance(state, dict):
            state['rag_results'] = rag_results
            state['agent_outputs']['treatment_advice'] = treatment_advice
            state['metadata']['treatments_retrieved'] = len(rag_results)
        else:
            state.rag_results = rag_results
            state.agent_outputs['treatment_advice'] = treatment_advice
            state.metadata['treatments_retrieved'] = len(rag_results)
        
        logger.info(f"[{self.name}] Treatment advice complete (length: {len(treatment_advice)})")
        
        return state