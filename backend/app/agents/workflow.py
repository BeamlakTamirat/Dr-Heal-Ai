from typing import Dict, Any, Literal
import logging
from langgraph.graph import StateGraph, END

from app.agents.state import AgentState
from app.agents.symptom_analyzer import SymptomAnalyzerAgent
from app.agents.disease_expert import DiseaseExpertAgent
from app.agents.treatment_advisor import TreatmentAdvisorAgent
from app.agents.emergency_triage import EmergencyTriageAgent

logger = logging.getLogger(__name__)


class MedicalWorkflow:
    def __init__(self):
        logger.info("Initializing Medical Workflow")
        
        self.symptom_analyzer = SymptomAnalyzerAgent()
        self.disease_expert = DiseaseExpertAgent()
        self.treatment_advisor = TreatmentAdvisorAgent()
        self.emergency_triage = EmergencyTriageAgent()
        
        self.graph = self._build_graph()
        
        logger.info("Medical Workflow initialized successfully")
    
    
    def _route_query(self, state: Dict[str, Any]) -> Literal["symptom_analyzer", "disease_expert", "treatment_advisor", "emergency_triage"]:
        if isinstance(state, AgentState):
            query = state.query.lower()
        else:
            query = state.get('query', '').lower()
        
        emergency_keywords = [
            'chest pain', 'difficulty breathing', "can't breathe",
            'severe bleeding', 'unconscious', 'seizure',
            'severe headache', 'sudden weakness', 'stroke',
            'heart attack', 'severe', 'emergency'
        ]
        
        if any(keyword in query for keyword in emergency_keywords):
            logger.info("Routing to EmergencyTriage (emergency detected)")
            return "emergency_triage"
        
        disease_keywords = [
            'what is', 'tell me about', 'explain', 'information about',
            'what are the symptoms of', 'causes of', 'how does'
        ]
        
        if any(keyword in query for keyword in disease_keywords):
            logger.info("Routing to DiseaseExpert (disease info query)")
            return "disease_expert"
        
        treatment_keywords = [
            'how to treat', 'treatment for', 'what should i do',
            'how to cure', 'remedy', 'medication', 'medicine'
        ]
        
        if any(keyword in query for keyword in treatment_keywords):
            logger.info("Routing to TreatmentAdvisor (treatment query)")
            return "treatment_advisor"
        
        logger.info("Routing to SymptomAnalyzer (symptom description)")
        return "symptom_analyzer"
    
    def _symptom_analyzer_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.symptom_analyzer.process(state)
    
    
    def _disease_expert_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.disease_expert.process(state)
    
    
    def _treatment_advisor_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.treatment_advisor.process(state)
    
    
    def _emergency_triage_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self.emergency_triage.process(state)
    
    
    def _format_response(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Formatting final response")
        
        # Handle both AgentState and dict
        if isinstance(state, dict):
            agent_outputs = state.get('agent_outputs', {})
        else:
            agent_outputs = state.agent_outputs
        
        # Get the response from whichever agent processed it
        response = (
            agent_outputs.get('symptom_analysis') or
            agent_outputs.get('disease_info') or
            agent_outputs.get('treatment_advice') or
            agent_outputs.get('emergency_triage') or
            'No response generated'
        )
        
        # Update state
        if isinstance(state, dict):
            state['final_response'] = response
        else:
            state.final_response = response
        
        logger.info(f"Final response formatted (length: {len(response)})")
        
        return state
    
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        
        workflow.add_node("symptom_analyzer", self._symptom_analyzer_node)
        workflow.add_node("disease_expert", self._disease_expert_node)
        workflow.add_node("treatment_advisor", self._treatment_advisor_node)
        workflow.add_node("emergency_triage", self._emergency_triage_node)
        workflow.add_node("format_response", self._format_response)
        
        workflow.set_conditional_entry_point(
            self._route_query,
            {
                "symptom_analyzer": "symptom_analyzer",
                "disease_expert": "disease_expert",
                "treatment_advisor": "treatment_advisor",
                "emergency_triage": "emergency_triage"
            }
        )
        
        workflow.add_edge("symptom_analyzer", "format_response")
        workflow.add_edge("disease_expert", "format_response")
        workflow.add_edge("treatment_advisor", "format_response")
        workflow.add_edge("emergency_triage", "format_response")
        
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    
    def process(self, query: str) -> Dict[str, Any]:
        logger.info(f"Processing query: '{query}'")
        
        initial_state = AgentState(
            query=query,
            rag_results=[],
            agent_outputs={},
            metadata={}
        )
        
        final_state = self.graph.invoke(initial_state.dict())
        
        logger.info("Workflow complete")
        
        return final_state


_workflow = None


def get_workflow() -> MedicalWorkflow:
    
    global _workflow
    
    if _workflow is None:
        logger.info("Creating global workflow instance")
        _workflow = MedicalWorkflow()
    
    return _workflow