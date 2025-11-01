from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentState(BaseModel):
    
    query: str = Field(..., description="User's medical query")
    
    query_type: Optional[str] = Field(None, description="Detected query type")
    
    rag_results: List[Dict[str, Any]] = Field(default_factory=list, description="RAG retrieval results")
    
    agent_outputs: Dict[str, Any] = Field(default_factory=dict, description="Outputs from each agent")
    
    final_response: Optional[str] = Field(None, description="Final response to user")
    
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    class Config:
        arbitrary_types_allowed = True