# 🏗️ Dr.Heal AI - System Architecture

## Table of Contents
- [Overview](#overview)
- [Multi-Agent System Design](#multi-agent-system-design)
- [Agent Specifications](#agent-specifications)
- [Orchestration Layer](#orchestration-layer)
- [Tool Integration](#tool-integration)
- [Data Flow](#data-flow)
- [State Management](#state-management)
- [Communication Protocol](#communication-protocol)

---

## Overview

Dr.Heal AI implements a sophisticated multi-agent architecture using **LangGraph** for orchestration. The system coordinates four specialized AI agents, each with distinct roles and capabilities, to provide comprehensive medical consultation services.

### Design Principles

1. **Separation of Concerns**: Each agent handles a specific medical domain
2. **Composability**: Agents can be combined in different workflows
3. **Shared Knowledge**: All agents access the same medical knowledge base
4. **Intelligent Routing**: Queries are routed to the most appropriate agent
5. **Stateful Communication**: Agents share context through a common state object

---

## Multi-Agent System Design

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Query Input                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Orchestrator                        │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Conditional Entry Point                        │ │
│  │                  (Query Router)                             │ │
│  │                                                              │ │
│  │  Analyzes query keywords to determine routing:              │ │
│  │  • Emergency keywords → EmergencyTriageAgent                │ │
│  │  • Disease info keywords → DiseaseExpertAgent               │ │
│  │  • Treatment keywords → TreatmentAdvisorAgent               │ │
│  │  • Default → SymptomAnalyzerAgent                           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Symptom    │  │   Disease    │  │  Treatment   │         │
│  │   Analyzer   │  │   Expert     │  │   Advisor    │         │
│  │              │  │              │  │              │         │
│  │ • Identifies │  │ • Provides   │  │ • Recommends │         │
│  │   symptoms   │  │   disease    │  │   evidence-  │         │
│  │ • Assesses   │  │   info       │  │   based      │         │
│  │   severity   │  │ • Explains   │  │   treatments │         │
│  │ • Lists      │  │   causes     │  │ • Self-care  │         │
│  │   conditions │  │ • Diagnosis  │  │   measures   │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                   │
│  ┌──────────────┐                                               │
│  │  Emergency   │                                               │
│  │   Triage     │                                               │
│  │              │                                               │
│  │ • Detects    │                                               │
│  │   emergencies│                                               │
│  │ • Urgency    │                                               │
│  │   assessment │                                               │
│  │ • Immediate  │                                               │
│  │   actions    │                                               │
│  └──────────────┘                                               │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              Response Formatter Node                        │ │
│  │  Aggregates agent outputs into final response               │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Final Response to User                      │
└─────────────────────────────────────────────────────────────────┘
```

### Agent Collaboration Flow

```
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│  Query Router (Conditional Logic)       │
│  • Keyword matching                     │
│  • Intent classification                │
└──────┬──────────────────────────────────┘
       │
       ├─────────────┬─────────────┬─────────────┐
       ▼             ▼             ▼             ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Symptom  │  │ Disease  │  │Treatment │  │Emergency │
│ Analyzer │  │ Expert   │  │ Advisor  │  │ Triage   │
└────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │             │             │             │
     │             │             │             │
     └─────────────┴─────────────┴─────────────┘
                   │
                   ▼
         ┌─────────────────┐
         │  Shared State   │
         │  • query        │
         │  • rag_results  │
         │  • agent_outputs│
         │  • metadata     │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Tools Execution │
         │  • RAG Retrieval│
         │  • Web Search   │
         │  • LLM Generate │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Format Response │
         └────────┬────────┘
                  │
                  ▼
         ┌─────────────────┐
         │ Final Response  │
         └─────────────────┘
```

---

## Agent Specifications

### 1. SymptomAnalyzerAgent

**Role**: Analyzes user-reported symptoms and assesses their severity

**Capabilities**:
- Identifies and categorizes symptoms
- Assesses severity (Mild/Moderate/Severe)
- Lists possible conditions based on symptoms
- Provides immediate recommendations
- Detects red flags requiring urgent attention

**Input Processing**:
```python
{
    "query": "I have a headache and fever for 2 days",
    "rag_results": [],  # Populated by RAG tool
    "agent_outputs": {},
    "metadata": {}
}
```

**Output Structure**:
```python
{
    "symptom_analysis": """
    **IDENTIFIED SYMPTOMS:**
    - Headache (duration: 2 days)
    - Fever (duration: 2 days)
    
    **SEVERITY ASSESSMENT:**
    - Overall severity: Moderate
    - Justification: Persistent symptoms for 2 days
    
    **POSSIBLE CONDITIONS:**
    1. Viral infection (flu, common cold)
    2. Bacterial infection
    3. Tension headache with coincidental fever
    
    **IMMEDIATE RECOMMENDATIONS:**
    - Rest and hydration
    - Monitor temperature
    - OTC pain relievers if needed
    
    **RED FLAGS:**
    - Fever >103°F (39.4°C)
    - Severe headache with stiff neck
    - Confusion or altered consciousness
    """
}
```

**Prompt Template**:
- Structured analysis format
- Emphasis on safety and red flags
- Clear severity classification
- Actionable recommendations

---

### 2. DiseaseExpertAgent

**Role**: Provides comprehensive information about medical conditions

**Capabilities**:
- Explains disease mechanisms
- Lists symptoms and progression
- Describes causes and risk factors
- Outlines diagnosis procedures
- Explains treatment options
- Discusses prevention strategies

**Input Processing**:
```python
{
    "query": "What is diabetes?",
    "rag_results": [],  # Medical knowledge about diabetes
    "agent_outputs": {},
    "metadata": {}
}
```

**Output Structure**:
```python
{
    "disease_info": """
    **DISEASE OVERVIEW:**
    Diabetes is a chronic condition affecting blood sugar regulation...
    
    **SYMPTOMS:**
    - Increased thirst and urination
    - Unexplained weight loss
    - Fatigue
    
    **CAUSES & RISK FACTORS:**
    - Type 1: Autoimmune destruction of insulin-producing cells
    - Type 2: Insulin resistance, often linked to obesity
    
    **DIAGNOSIS:**
    - Fasting blood glucose test
    - HbA1c test
    - Oral glucose tolerance test
    
    **TREATMENT OPTIONS:**
    - Type 1: Insulin therapy
    - Type 2: Lifestyle changes, oral medications, insulin
    
    **PREVENTION:**
    - Maintain healthy weight
    - Regular physical activity
    - Balanced diet
    
    **COMPLICATIONS:**
    - Cardiovascular disease
    - Kidney damage
    - Nerve damage
    """
}
```

**RAG Integration**:
- Retrieves 3 most relevant disease documents
- Filters by disease type metadata
- Combines knowledge base with LLM generation

---

### 3. TreatmentAdvisorAgent

**Role**: Recommends evidence-based treatments and self-care measures

**Capabilities**:
- Suggests immediate self-care actions
- Recommends OTC medications with dosages
- Provides home remedies
- Advises lifestyle adjustments
- Defines criteria for seeking medical care
- Sets expectations for recovery

**Input Processing**:
```python
{
    "query": "How to treat a sprained ankle?",
    "rag_results": [],  # Treatment protocols
    "agent_outputs": {},
    "metadata": {}
}
```

**Output Structure**:
```python
{
    "treatment_advice": """
    **IMMEDIATE SELF-CARE (RICE Protocol):**
    - Rest: Avoid weight-bearing activities
    - Ice: Apply for 15-20 minutes every 2-3 hours
    - Compression: Use elastic bandage
    - Elevation: Keep ankle above heart level
    
    **OTC MEDICATIONS:**
    - Ibuprofen 400mg every 6-8 hours (with food)
    - Acetaminophen 500mg every 6 hours (alternative)
    - Precautions: Avoid if allergic, stomach ulcers
    
    **HOME REMEDIES:**
    - Gentle range-of-motion exercises after 48 hours
    - Warm compresses after initial swelling subsides
    
    **LIFESTYLE ADJUSTMENTS:**
    - Use crutches if weight-bearing is painful
    - Wear supportive footwear
    - Avoid high-impact activities
    
    **WHEN TO SEE A DOCTOR:**
    - Unable to bear weight after 48 hours
    - Severe swelling or bruising
    - Numbness or tingling
    - No improvement after 1 week
    
    **RECOVERY TIMELINE:**
    - Mild sprain: 1-2 weeks
    - Moderate: 3-6 weeks
    - Severe: 3-6 months
    """
}
```

**Safety Features**:
- Clear contraindications for medications
- Emphasis on when professional care is needed
- Evidence-based recommendations only

---

### 4. EmergencyTriageAgent

**Role**: Identifies medical emergencies and provides urgent guidance

**Capabilities**:
- Detects emergency keywords
- Assesses urgency level (IMMEDIATE/URGENT/NON-URGENT)
- Provides step-by-step emergency instructions
- Lists critical warning signs
- Advises on actions to avoid
- Guides preparation for emergency responders

**Emergency Keywords**:
```python
[
    'chest pain', 'difficulty breathing', "can't breathe",
    'severe bleeding', 'unconscious', 'seizure',
    'severe headache', 'sudden weakness', 'stroke',
    'heart attack', 'allergic reaction', 'anaphylaxis',
    'severe burn', 'poisoning', 'overdose',
    'suicidal', 'severe injury', 'broken bone'
]
```

**Input Processing**:
```python
{
    "query": "I have severe chest pain and difficulty breathing",
    "rag_results": [],  # Emergency protocols
    "agent_outputs": {},
    "metadata": {}
}
```

**Output Structure**:
```python
{
    "emergency_triage": """
    ⚠️ **EMERGENCY ASSESSMENT:**
    - Is this a medical emergency? **YES**
    - Urgency level: **IMMEDIATE**
    - Reasoning: Chest pain + breathing difficulty = potential heart attack/PE
    
    🚨 **IMMEDIATE ACTIONS:**
    1. **CALL 911 IMMEDIATELY**
    2. Sit down and stay calm
    3. Loosen tight clothing
    4. If prescribed, take nitroglycerin
    5. Chew aspirin 325mg (if not allergic)
    
    ⚠️ **WARNING SIGNS:**
    - Pain radiating to arm, jaw, or back
    - Sweating, nausea, lightheadedness
    - Worsening breathing difficulty
    
    ❌ **DO NOT:**
    - Drive yourself to hospital
    - Eat or drink anything
    - Lie flat (sit upright instead)
    - Delay calling emergency services
    
    🏥 **WHILE WAITING FOR HELP:**
    - Sit in comfortable position
    - Stay calm, breathe slowly
    - Prepare list of medications
    - Unlock door for paramedics
    - Have someone stay with you
    """
}
```

**Detection Logic**:
```python
def detect_emergency(self, query: str) -> bool:
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in self.emergency_keywords)
```

---

## Orchestration Layer

### LangGraph Workflow Implementation

**File**: `backend/app/agents/workflow.py`

```python
class MedicalWorkflow:
    def __init__(self):
        # Initialize all agents
        self.symptom_analyzer = SymptomAnalyzerAgent()
        self.disease_expert = DiseaseExpertAgent()
        self.treatment_advisor = TreatmentAdvisorAgent()
        self.emergency_triage = EmergencyTriageAgent()
        
        # Build LangGraph workflow
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        workflow = StateGraph(AgentState)
        
        # Add agent nodes
        workflow.add_node("symptom_analyzer", self._symptom_analyzer_node)
        workflow.add_node("disease_expert", self._disease_expert_node)
        workflow.add_node("treatment_advisor", self._treatment_advisor_node)
        workflow.add_node("emergency_triage", self._emergency_triage_node)
        workflow.add_node("format_response", self._format_response)
        
        # Set conditional entry point (routing logic)
        workflow.set_conditional_entry_point(
            self._route_query,
            {
                "symptom_analyzer": "symptom_analyzer",
                "disease_expert": "disease_expert",
                "treatment_advisor": "treatment_advisor",
                "emergency_triage": "emergency_triage"
            }
        )
        
        # All agents flow to response formatter
        workflow.add_edge("symptom_analyzer", "format_response")
        workflow.add_edge("disease_expert", "format_response")
        workflow.add_edge("treatment_advisor", "format_response")
        workflow.add_edge("emergency_triage", "format_response")
        
        # End after formatting
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
```

### Routing Logic

```python
def _route_query(self, state: Dict[str, Any]) -> str:
    query = state.get('query', '').lower()
    
    # Priority 1: Emergency detection
    emergency_keywords = ['chest pain', 'difficulty breathing', ...]
    if any(keyword in query for keyword in emergency_keywords):
        return "emergency_triage"
    
    # Priority 2: Disease information
    disease_keywords = ['what is', 'tell me about', 'explain', ...]
    if any(keyword in query for keyword in disease_keywords):
        return "disease_expert"
    
    # Priority 3: Treatment queries
    treatment_keywords = ['how to treat', 'treatment for', ...]
    if any(keyword in query for keyword in treatment_keywords):
        return "treatment_advisor"
    
    # Default: Symptom analysis
    return "symptom_analyzer"
```

---

## Tool Integration

### 1. ChromaDB RAG Tool

**Purpose**: Retrieve relevant medical knowledge from vector database

**Implementation**:
```python
class MedicalVectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(
            name="medical_knowledge"
        )
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        query_embedding = self.embedding_model.encode(query)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        return results
```

**Usage in Agents**:
```python
# Each agent retrieves relevant context
rag_results = self.retrieve_knowledge(query=query, n_results=5)
context = self.format_context(rag_results)
```

### 2. DuckDuckGo Web Search Tool

**Purpose**: Fetch latest medical information from trusted sources

**Implementation**:
```python
class MedicalWebSearchTool:
    def search(self, query: str, max_results: int = 3) -> List[Dict]:
        medical_query = f"{query} site:nih.gov OR site:mayoclinic.org"
        results = DDGS().text(medical_query, max_results=max_results)
        return results
```

**Trusted Sources**:
- nih.gov (National Institutes of Health)
- mayoclinic.org (Mayo Clinic)
- who.int (World Health Organization)

### 3. Gemini LLM API

**Purpose**: Generate natural language responses

**Implementation**:
```python
class GeminiLLM:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
```

**Configuration**:
- Model: gemini-2.0-flash-exp
- Temperature: 0.7 (balanced creativity/consistency)
- Max tokens: 2048
- Safety settings: Block harmful content

---

## Data Flow

### Complete Request Flow

```
1. User sends query via Flutter app
   ↓
2. FastAPI receives request at /api/conversations/chat
   ↓
3. JWT authentication validates user
   ↓
4. Query passed to MedicalWorkflow.process()
   ↓
5. LangGraph router analyzes query keywords
   ↓
6. Appropriate agent selected (e.g., SymptomAnalyzer)
   ↓
7. Agent retrieves context from ChromaDB (RAG)
   ↓
8. Agent optionally searches web for latest info
   ↓
9. Agent formats prompt with context + query
   ↓
10. Gemini LLM generates response
   ↓
11. Agent updates shared state with output
   ↓
12. Response formatter aggregates agent outputs
   ↓
13. Final response saved to Supabase database
   ↓
14. Response returned to Flutter app
   ↓
15. UI displays response with agent badge
```

### State Transitions

```
Initial State:
{
    "query": "user input",
    "rag_results": [],
    "agent_outputs": {},
    "metadata": {}
}

After Agent Processing:
{
    "query": "user input",
    "rag_results": [
        {"document": "...", "metadata": {...}},
        ...
    ],
    "agent_outputs": {
        "symptom_analysis": "detailed analysis..."
    },
    "metadata": {
        "symptoms_retrieved": 5,
        "agent_used": "SymptomAnalyzer"
    }
}

Final State:
{
    "query": "user input",
    "rag_results": [...],
    "agent_outputs": {...},
    "metadata": {...},
    "final_response": "formatted response for user"
}
```

---

## State Management

### AgentState Schema

**File**: `backend/app/agents/state.py`

```python
from typing import List, Dict, Any
from pydantic import BaseModel

class AgentState(BaseModel):
    query: str                          # User's input query
    rag_results: List[Dict] = []        # Retrieved medical knowledge
    agent_outputs: Dict[str, str] = {}  # Outputs from each agent
    metadata: Dict[str, Any] = {}       # Additional context/metrics
    final_response: str = ""            # Formatted final response
```

### State Updates

Each agent updates the shared state:

```python
def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
    # Retrieve knowledge
    rag_results = self.retrieve_knowledge(query)
    state['rag_results'] = rag_results
    
    # Generate response
    analysis = self.generate_response(prompt)
    state['agent_outputs']['symptom_analysis'] = analysis
    
    # Add metadata
    state['metadata']['symptoms_retrieved'] = len(rag_results)
    state['metadata']['agent_used'] = self.name
    
    return state
```

---

## Communication Protocol

### Inter-Agent Communication

Agents communicate through **shared state** rather than direct messaging:

1. **State Initialization**: Workflow creates initial AgentState
2. **Agent Processing**: Selected agent reads state, processes query
3. **State Update**: Agent writes results back to state
4. **State Passing**: Updated state flows to next node
5. **Response Aggregation**: Final node reads all agent outputs

### Benefits of Shared State

- **Simplicity**: No complex message passing
- **Traceability**: Full history in state object
- **Flexibility**: Easy to add new agents
- **Debugging**: State can be inspected at any point
- **Persistence**: State can be saved for analysis

---

## Performance Considerations

### Optimization Strategies

1. **Singleton Pattern**: Agents initialized once, reused
2. **RAG Caching**: Frequently accessed documents cached
3. **Async Processing**: Non-blocking I/O operations
4. **Connection Pooling**: Database connections reused
5. **Response Streaming**: Large responses streamed to client

### Scalability

- **Horizontal Scaling**: Multiple backend instances on Railway
- **Load Balancing**: Railway handles request distribution
- **Database Pooling**: Supabase connection pooling
- **Stateless Design**: No server-side session storage

---

## Error Handling

### Agent-Level Error Handling

```python
try:
    rag_results = self.retrieve_knowledge(query)
except Exception as e:
    logger.error(f"RAG retrieval failed: {e}")
    rag_results = []  # Graceful degradation

try:
    response = self.generate_response(prompt)
except Exception as e:
    logger.error(f"LLM generation failed: {e}")
    response = "I apologize, but I'm having trouble processing your request."
```

### Workflow-Level Error Handling

- **Retry Logic**: Failed LLM calls retried with exponential backoff
- **Timeout Protection**: Maximum execution time per agent
- **Fallback Responses**: Default responses if all agents fail
- **Error Logging**: All errors logged for debugging

---

## Monitoring & Observability

### Logging Strategy

```python
logger.info(f"[{self.name}] Processing query: {query}")
logger.info(f"[{self.name}] Retrieved {len(rag_results)} documents")
logger.info(f"[{self.name}] Analysis complete (length: {len(analysis)})")
```

### Metrics Tracked

- Agent selection distribution
- RAG retrieval counts
- Response generation times
- Error rates per agent
- User query patterns

---

**This architecture enables Dr.Heal AI to provide intelligent, context-aware medical consultations through coordinated multi-agent collaboration.**
