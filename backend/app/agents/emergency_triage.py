from typing import Dict, Any
import logging

from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)


class EmergencyTriageAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="EmergencyTriage",
            role="Identifies medical emergencies and provides urgent guidance"
        )
        
        self.emergency_keywords = [
            'chest pain', 'difficulty breathing', 'can\'t breathe',
            'severe bleeding', 'unconscious', 'seizure',
            'severe headache', 'sudden weakness', 'stroke',
            'heart attack', 'allergic reaction', 'anaphylaxis',
            'severe burn', 'poisoning', 'overdose',
            'suicidal', 'severe injury', 'broken bone'
        ]
        
        self.prompt_template = """You are an emergency medical triage specialist. Assess the urgency of this situation.

CONTEXT FROM MEDICAL KNOWLEDGE BASE:
{context}

USER'S SITUATION:
{query}

Provide URGENT assessment:

1. **EMERGENCY ASSESSMENT:**
   - Is this a medical emergency? YES / NO
   - Urgency level: IMMEDIATE / URGENT / NON-URGENT
   - Reasoning for assessment

2. **IMMEDIATE ACTIONS:**
   - What to do RIGHT NOW
   - Step-by-step instructions
   - Who to call (911, doctor, etc.)

3. **WARNING SIGNS:**
   - Critical symptoms to watch for
   - Signs of worsening condition
   - When to call emergency services

4. **DO NOT:**
   - Actions to avoid
   - Common mistakes
   - Dangerous interventions

5. **WHILE WAITING FOR HELP:**
   - Safe positioning
   - Comfort measures
   - What information to prepare for emergency responders

If this is an emergency, use clear, bold language. Be direct and action-oriented."""
    
    
    def detect_emergency(self, query: str) -> bool:
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.emergency_keywords)
    
    
    def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if isinstance(state, dict):
            query = state['query']
        else:
            query = state.query
        
        logger.info(f"[{self.name}] Processing query: {query}")
        
        is_potential_emergency = self.detect_emergency(query)
        
        rag_results = self.retrieve_knowledge(
            query=query,
            n_results=3
        )
        
        context = self.format_context(rag_results)
        
        prompt = self.prompt_template.format(
            context=context,
            query=query
        )
        
        triage_assessment = self.generate_response(prompt)
        
        if isinstance(state, dict):
            state['rag_results'] = rag_results
            state['agent_outputs']['emergency_triage'] = triage_assessment
            state['metadata']['is_potential_emergency'] = is_potential_emergency
            state['metadata']['emergency_keywords_detected'] = is_potential_emergency
        else:
            state.rag_results = rag_results
            state.agent_outputs['emergency_triage'] = triage_assessment
            state.metadata['is_potential_emergency'] = is_potential_emergency
            state.metadata['emergency_keywords_detected'] = is_potential_emergency
        
        logger.info(f"[{self.name}] Triage complete. Emergency detected: {is_potential_emergency}")
        
        return state