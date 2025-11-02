# Dr.Heal AI - Multi-Agent Medical Assistant

> **AAIDC - Module 2**

An intelligent medical assistant powered by 4 specialized AI agents orchestrated with LangGraph. The system uses RAG (Retrieval-Augmented Generation) with medical knowledge base and web search to provide accurate, context-aware medical information.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2.59-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-teal)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

---

## 🎯 Project Overview

Dr.Heal AI demonstrates advanced agentic AI capabilities through:
- **Multi-agent collaboration** with 4 specialized medical agents
- **LangGraph orchestration** for intelligent query routing
- **RAG system** with ChromaDB vector store and 20 medical documents
- **External tool integration** including web search for latest medical info
- **Real-time medical assistance** via FastAPI endpoints

---

## 🏗️ Architecture

```
User Query
    ↓
[Router Agent]
    ↓
    ├─→ [SymptomAnalyzer] ─→ Analyzes symptoms, assesses severity
    ├─→ [DiseaseExpert] ───→ Provides disease information
    ├─→ [TreatmentAdvisor] → Recommends treatments
    └─→ [EmergencyTriage] ─→ Detects emergencies
         ↓
    [Tools Layer]
         ├─→ RAG System (ChromaDB + Embeddings)
         ├─→ LLM (Google Gemini)
         └─→ Web Search (DuckDuckGo)
         ↓
    [Response Formatter]
         ↓
    Final Response
```

---

## 🤖 Specialized Agents

### 1. **SymptomAnalyzer**
- Analyzes user-reported symptoms
- Assesses severity (Mild/Moderate/Severe)
- Identifies possible conditions
- Provides immediate recommendations

### 2. **DiseaseExpert**
- Explains diseases and conditions
- Describes symptoms and causes
- Provides prevention strategies
- Educational and reassuring

### 3. **TreatmentAdvisor**
- Recommends treatment options
- Suggests self-care measures
- Advises when to seek medical help
- Practical and safety-focused

### 4. **EmergencyTriage**
- Detects medical emergencies
- Provides urgent action steps
- Prioritizes immediate care
- Critical for life-threatening situations

---

## 🛠️ Tools & Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestration** | LangGraph 0.2.59 | Multi-agent workflow management |
| **LLM** | Google Gemini 2.5 Flash | Response generation |
| **Vector Store** | ChromaDB 0.5.23 | Medical knowledge retrieval |
| **Embeddings** | sentence-transformers | Document embedding |
| **Web Search** | DuckDuckGo Search | Latest medical information |
| **API** | FastAPI 0.115 | REST endpoints |
| **Frontend** | Flutter | Mobile & web UI |

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Google Gemini API key

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/BeamlakTamirat/Dr-Heal-Ai-module-2.git
cd Dr-Heal-Ai-module-2/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

5. **Load medical knowledge**
```bash
python load_medical_data.py
```

6. **Run the server**
```bash
uvicorn app.main:app --reload
```

Server will start at `http://localhost:8000`

---

## 🚀 Usage

### API Endpoints

#### 1. Chat Endpoint
```bash
POST /api/chat
Content-Type: application/json

{
  "query": "I have fever and cough for 3 days",
  "chat_type": "symptoms"
}
```

**Response:**
```json
{
  "response": "**IDENTIFIED SYMPTOMS:**\n- Fever: Present for 3 days\n- Cough: Present for 3 days\n\n**SEVERITY ASSESSMENT:**\n- Overall severity: Moderate...",
  "agent_used": "SymptomAnalyzer",
  "rag_sources": 5,
  "web_sources": 3
}
```

#### 2. Health Check
```bash
GET /health
```

### Example Queries

**Symptom Analysis:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "I have headache and dizziness", "chat_type": "symptoms"}'
```

**Disease Information:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is pneumonia?", "chat_type": "disease"}'
```

**Treatment Advice:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "How to treat a cold?", "chat_type": "treatment"}'
```

**Emergency Detection:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Severe chest pain and difficulty breathing", "chat_type": "emergency"}'
```

---

## 🧪 Testing

Run the test suite:
```bash
python test_agents.py
```

**Expected Output:**
```
✅ TEST 1: SYMPTOM QUERY - PASSED
✅ TEST 2: DISEASE QUERY - PASSED
✅ TEST 3: TREATMENT QUERY - PASSED
✅ TEST 4: EMERGENCY QUERY - PASSED

Multi-agent system is working perfectly!
```

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── agents/
│   │   ├── base_agent.py          # Base agent class
│   │   ├── state.py                # Agent state management
│   │   ├── workflow.py             # LangGraph orchestration
│   │   ├── symptom_analyzer.py     # Symptom analysis agent
│   │   ├── disease_expert.py       # Disease information agent
│   │   ├── treatment_advisor.py    # Treatment advice agent
│   │   ├── emergency_triage.py     # Emergency detection agent
│   │   └── tools/
│   │       └── web_search.py       # Web search tool
│   ├── api/
│   │   └── chat.py                 # Chat endpoints
│   ├── llm/
│   │   ├── gemini.py               # Gemini LLM integration
│   │   └── rag_chain.py            # RAG chain
│   ├── rag/
│   │   ├── embeddings.py           # Embedding model
│   │   ├── vectorstore.py          # ChromaDB integration
│   │   └── medical_rag.py          # Medical RAG system
│   └── main.py                     # FastAPI app
├── data/
│   └── medical_knowledge/          # Medical documents
├── chroma_db/                      # Vector database
├── test_agents.py                  # Test suite
├── requirements.txt                # Dependencies
└── .env.example                    # Environment template
```

---

## 🔑 Environment Variables

Create a `.env` file with:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
CHROMA_DB_PATH=./chroma_db
MEDICAL_DATA_PATH=./data/medical_knowledge
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

---

## 🎓 Module 2 Requirements Met

| Requirement | Implementation | Status |
|-------------|----------------|--------|
| **Multi-agent system (3+)** | 4 specialized agents | ✅ |
| **LangGraph orchestration** | Conditional routing workflow | ✅ |
| **Tool integration (3+)** | RAG, LLM, Web Search | ✅ |
| **Agent collaboration** | Shared state, sequential processing | ✅ |
| **Documentation** | Comprehensive README | ✅ |

---





---
