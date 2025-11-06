# 🏥 Dr.Heal AI - Intelligent Medical Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flutter 3.0+](https://img.shields.io/badge/flutter-3.0+-blue.svg)](https://flutter.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.59-orange.svg)](https://github.com/langchain-ai/langgraph)

> **A production-ready, multi-agent AI system for medical consultation and health guidance**


  


[![Download APK](https://img.shields.io/badge/Download-Android_APK-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://github.com/BeamlakTamirat/Dr-Heal-Ai/releases)

**Get the latest version for Android devices**



**🔥Dr.Heal AI** - is an intelligent medical assistant that leverages a sophisticated multi-agent architecture to provide personalized health consultations. Built with LangGraph orchestration, the system coordinates specialized AI agents to analyze symptoms, provide disease information, recommend treatments, and handle medical emergencies.

---

## 🎯 Project Overview

### What is Dr.Heal AI?

Dr.Heal AI is a comprehensive healthcare assistant that combines:
- **Multi-Agent AI System**: 4 specialized agents working in coordination
- **Medical Knowledge Base**: RAG-powered system with ChromaDB vector storage
- **Real-time Web Search**: Latest medical information from trusted sources
- **Secure Authentication**: JWT-based user management
- **Beautiful Mobile UI**: Cross-platform Flutter application
- **Production Deployment**: Containerized backend on Railway.app

### Key Features

🤖 **Intelligent Agent System**
- Symptom analysis and severity assessment
- Comprehensive disease information
- Evidence-based treatment recommendations
- Emergency triage and urgent care guidance

🔒 **Enterprise-Grade Security**
- JWT authentication with bcrypt password hashing
- Rate limiting (100 requests/minute)
- Input validation and sanitization
- Secure API key management

📱 **Modern User Experience**
- Beautiful Material Design UI
- Real-time chat interface
- Conversation history
- Agent-specific response badges
- Offline-capable architecture

🧪 **Production-Ready**
- Comprehensive test suite (70%+ coverage)
- Docker containerization
- CI/CD with Railway
- Monitoring and logging
- Error handling and retry logic

---

## 🏗️ System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Flutter Mobile App                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │   Auth   │  │   Chat   │  │ History  │  │ Profile  │     │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS/REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Railway)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LangGraph Orchestration                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │   │
│  │  │  Symptom    │  │  Disease    │  │ Treatment   │   │   │
│  │  │  Analyzer   │  │  Expert     │  │  Advisor    │   │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘   │   │
│  │  ┌─────────────┐                                     │   │
│  │  │ Emergency   │    Shared State & Communication     │   │
│  │  │  Triage     │                                     │   │
│  │  └─────────────┘                                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  ChromaDB    │  │  DuckDuckGo  │  │   Gemini     │       │
│  │  (RAG)       │  │  Web Search  │  │   LLM API    │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Supabase PostgreSQL                      │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  Users   │  │Conversations │  │   Messages   │           │
│  └──────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Multi-Agent Workflow

```
User Query
    │
    ▼
┌─────────────────┐
│ Query Router    │ ◄── Intelligent routing based on keywords
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Symptom │ │Disease │ │Treatment│ │Emergency│
│Analyzer│ │Expert  │ │Advisor │ │Triage  │
└───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘
    │          │          │          │
    └──────────┴──────────┴──────────┘
                 │
                 ▼
         ┌──────────────┐
         │   RAG Tool   │ ◄── Medical knowledge retrieval
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │  Web Search  │ ◄── Latest medical info
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │ Gemini LLM   │ ◄── Response generation
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │Final Response│
         └──────────────┘
```

---

<details>
<summary><b>🚀 Quick Start</b> (Click to expand)</summary>

### Prerequisites

**Backend:**
- Python 3.11+
- PostgreSQL (via Supabase)
- Google Gemini API key

**Frontend:**
- Flutter 3.0+
- Android Studio / Xcode
- Android/iOS device or emulator

### Installation

#### 1. Clone Repository

```bash
git clone https://github.com/BeamlakTamirat/Dr-Heal-Ai.git
cd Dr-Heal-Ai
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys:
# - GEMINI_API_KEY
# - SUPABASE_URL
# - SUPABASE_KEY
# - JWT_SECRET_KEY

# Run backend
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
flutter pub get

# Update API URL in lib/core/constants/api_constants.dart
# For local development: http://localhost:8000
# For production: https://your-railway-url.up.railway.app

# Run app
flutter run
```

</details>

---

## 📚 Documentation

Comprehensive documentation is available in the `docs/` folder:

| Document | Description |
|----------|-------------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Multi-agent system design and agent roles |
| [DEPLOYMENT.md](docs/DEPLOYMENT.md) | Production deployment guide (Railway) |
| [API.md](docs/API.md) | Complete API reference and endpoints |
| [TESTING.md](docs/TESTING.md) | Testing strategy and coverage |
| [SECURITY.md](docs/SECURITY.md) | Security measures and guardrails |
| [MODULE_COMPLIANCE.md](docs/MODULE_COMPLIANCE.md) | AAIDC certification requirements |

---

<details>
<summary><b>🛠️ Technology Stack</b> (Click to expand)</summary>

### Backend
- **Framework**: FastAPI 0.115.6
- **Orchestration**: LangGraph 0.2.59
- **LLM**: Google Gemini 2.0 Flash
- **Vector DB**: ChromaDB 0.5.23
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT with bcrypt
- **Web Search**: DuckDuckGo Search API
- **Deployment**: Docker + Railway.app

### Frontend
- **Framework**: Flutter 3.0+
- **State Management**: Riverpod
- **HTTP Client**: Dio
- **Storage**: Shared Preferences
- **UI**: Material Design 3

### DevOps
- **Containerization**: Docker (multi-stage builds)
- **CI/CD**: GitHub + Railway auto-deploy
- **Monitoring**: Railway logs + health checks
- **Testing**: Pytest (backend), Flutter test (frontend)

---
</details>

## 🎯 Module 2 Compliance (Multi-Agent System)

### ✅ Required Components

**1. Multi-Agent System (4 agents)**
- ✅ **SymptomAnalyzerAgent**: Analyzes symptoms and assesses severity
- ✅ **DiseaseExpertAgent**: Provides comprehensive disease information
- ✅ **TreatmentAdvisorAgent**: Recommends evidence-based treatments
- ✅ **EmergencyTriageAgent**: Identifies emergencies and provides urgent guidance

**2. Orchestration Framework**
- ✅ **LangGraph**: State-based workflow orchestration
- ✅ **Conditional routing**: Intelligent query routing to appropriate agent
- ✅ **Shared state**: AgentState for inter-agent communication

**3. Tool Integration (3+ tools)**
- ✅ **ChromaDB RAG**: Medical knowledge retrieval with vector search
- ✅ **DuckDuckGo Web Search**: Real-time medical information from trusted sources
- ✅ **Gemini LLM API**: Advanced language understanding and generation

**4. Communication Protocol**
- ✅ **Shared state management**: AgentState with query, rag_results, agent_outputs, metadata
- ✅ **Sequential processing**: Each agent updates state for next agent
- ✅ **Response aggregation**: Final response formatting from agent outputs

---

## 🏭 Module 3 Compliance (Production-Ready)

### ✅ Required Components

**1. Comprehensive Testing Suite**
- ✅ **Unit tests**: Individual agent functions and tools
- ✅ **Integration tests**: Agent-to-agent communication (test_auth.py, test_conversations.py)
- ✅ **End-to-end tests**: Complete workflows
- ✅ **Test coverage**: 70%+ for core functionality

**2. Safety & Security Guardrails**
- ✅ **Input validation**: Pydantic models for all API inputs
- ✅ **Authentication**: JWT tokens with bcrypt password hashing
- ✅ **Rate limiting**: 100 requests/minute per IP
- ✅ **Error handling**: Try-catch blocks throughout codebase
- ✅ **Logging**: Comprehensive logging for debugging and compliance

**3. User Interface**
- ✅ **Flutter mobile app**: Cross-platform iOS/Android
- ✅ **Intuitive design**: Material Design 3 with clear navigation
- ✅ **Real-time chat**: Interactive conversation interface
- ✅ **Error messages**: User-friendly error handling and guidance

**4. Resilience & Monitoring**
- ✅ **Retry logic**: Exponential backoff for failed API calls
- ✅ **Timeout handling**: Prevents long-running workflows
- ✅ **Graceful degradation**: Fallback responses on agent failure
- ✅ **Health checks**: `/health` endpoint for monitoring
- ✅ **Logging**: Structured logging for all failures and retries

**5. Professional Documentation**
- ✅ **System overview**: This README with architecture diagrams
- ✅ **Deployment guide**: Complete Railway deployment instructions
- ✅ **API specifications**: FastAPI auto-generated docs at `/docs`
- ✅ **Maintenance guide**: Logging, health checks, troubleshooting
- ✅ **Troubleshooting**: Common issues and recovery steps

---

## 📊 Project Statistics

- **Total Lines of Code**: ~15,000+
- **Backend Files**: 35+ Python modules
- **Frontend Files**: 50+ Dart files
- **Test Coverage**: 70%+
- **API Endpoints**: 15+
- **Agents**: 4 specialized agents
- **Tools**: 3+ integrated tools
- **Deployment Time**: ~6 minutes
- **Response Time**: <2 seconds average

---

## 🎥 Demo

### Live Deployment
- **Backend API**: https://dr-heal-ai-production.up.railway.app
- **API Docs**: https://dr-heal-ai-production.up.railway.app/docs
- **Health Check**: https://dr-heal-ai-production.up.railway.app/health


---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## 👥 Authors

- **Beamlak Tamirat** - *Lead Developer* - [GitHub](https://github.com/BeamlakTamirat)

---

---

## 🔮 Future Enhancements

- [ ] Voice input for symptom description
- [ ] Multi-language support
- [ ] Medical image analysis
- [ ] Prescription tracking
- [ ] Appointment scheduling
- [ ] Telemedicine integration
- [ ] Wearable device integration
- [ ] Advanced analytics dashboard

---

