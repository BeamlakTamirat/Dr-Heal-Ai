# Dr.Heal AI Backend

AI-powered medical assistant backend built with FastAPI, LangChain, and LangGraph.

## Tech Stack

- FastAPI - Web framework
- LangChain - LLM application framework
- LangGraph - Multi-agent orchestration
- Chroma DB - Vector database
- Google Gemini - LLM
- Supabase - Database

# Project Structure
backend/
├── app/
│   ├── api/        - API endpoints
│   ├── agents/     - LangGraph AI agents
│   ├── rag/        - RAG system
│   ├── llm/        - Gemini integration
│   ├── models/     - Data models
│   └── services/   - Business logic
├── data/           - Medical knowledge
├── chroma_db/      - Vector database storage
└── requirements.txt