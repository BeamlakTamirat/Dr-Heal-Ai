# 🚀 Dr.Heal AI - Deployment Guide

## Table of Contents
- [Overview](#overview)
- [Local Development Setup](#local-development-setup)
- [Production Deployment (Railway)](#production-deployment-railway)
- [Environment Variables](#environment-variables)
- [Docker Configuration](#docker-configuration)
- [Database Setup](#database-setup)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

---

## Overview

Dr.Heal AI is deployed using a containerized architecture on **Railway.app**, providing automatic scaling, continuous deployment, and built-in monitoring. The system consists of:

- **Backend**: FastAPI application with LangGraph agents
- **Database**: Supabase PostgreSQL
- **Vector Store**: ChromaDB (persistent volume)
- **Frontend**: Flutter mobile application

---

## Local Development Setup

### Backend Setup

**Prerequisites:**
- Python 3.11+
- PostgreSQL (via Supabase account)
- Google Gemini API key

**Steps:**

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Configure environment variables (see Environment Variables section)

# 6. Run database migrations (if needed)
python -m app.database.connection

# 7. Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify Backend:**
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs
- Root endpoint: http://localhost:8000/

### Frontend Setup

**Prerequisites:**
- Flutter 3.0+
- Android Studio / Xcode
- Android/iOS emulator or physical device

**Steps:**

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
flutter pub get

# 3. Update API URL in lib/core/constants/api_constants.dart
# For local development:
static const String _productionUrl = 'http://localhost:8000';

# 4. Run app
flutter run

# Or specify device
flutter run -d <device-id>
```

**Verify Frontend:**
- App should launch on emulator/device
- Registration should work
- Chat interface should be accessible

---

## Production Deployment (Railway)

### Step 1: Prepare Repository

**1. Ensure all files are committed:**
```bash
git add .
git commit -m "Prepare for deployment"
git push origin main
```

**2. Required files:**
- ✅ `backend/Dockerfile` - Multi-stage Docker build
- ✅ `backend/requirements.txt` - Python dependencies
- ✅ `backend/.dockerignore` - Exclude unnecessary files
- ✅ `backend/railway.toml` - Railway configuration (optional)

### Step 2: Create Railway Project

**1. Sign up/Login:**
- Go to https://railway.app
- Sign in with GitHub

**2. Create New Project:**
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose `Dr-Heal-Ai` repository
- Select `main` branch

**3. Configure Service:**
- Railway will auto-detect Dockerfile
- Set root directory: `backend`
- Click "Deploy"

### Step 3: Configure Environment Variables

**In Railway Dashboard → Variables tab, add:**

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here
JWT_SECRET_KEY=your_random_secret_key_here

# Optional (Railway sets PORT automatically)
# PORT=8080  # Don't set this manually
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Configure Custom Start Command

**In Railway Dashboard → Settings → Deploy:**

**Custom Start Command:**
```bash
sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"
```

This ensures the PORT variable is properly expanded.

### Step 5: Configure Networking

**In Railway Dashboard → Settings → Networking:**

**1. Public Networking:**
- Enable public networking
- Railway will assign: `your-app.up.railway.app`
- Port: 8080 (auto-detected)

**2. Custom Domain (Optional):**
- Add your custom domain
- Configure DNS CNAME record
- Railway handles SSL automatically

### Step 6: Configure Volumes (ChromaDB)

**In Railway Dashboard → Settings → Volumes:**

**1. Create Volume:**
- Click "New Volume"
- Mount path: `/app/chroma_db`
- Size: 1GB (sufficient for medical knowledge base)

**2. Verify in Dockerfile:**
```dockerfile
# Create directories
RUN mkdir -p /app/chroma_db /app/data/medical_knowledge && \
    chmod -R 755 /app/chroma_db /app/data/medical_knowledge
```

### Step 7: Deploy

**1. Trigger Deployment:**
- Railway auto-deploys on git push
- Or manually: Click "Redeploy" in Deployments tab

**2. Monitor Build:**
- Watch build logs in real-time
- Build time: ~2-6 minutes
- Look for: "Build time: XXX seconds"

**3. Monitor Deployment:**
- Check deploy logs
- Look for: "Application startup complete"
- Verify: "Uvicorn running on http://0.0.0.0:8080"

**4. Verify Deployment:**
```bash
# Health check
curl https://your-app.up.railway.app/health

# Expected response:
{"status":"healthy"}

# API root
curl https://your-app.up.railway.app/

# Expected: API information
```

---

## Environment Variables

### Required Variables

| Variable | Description | Example | Where to Get |
|----------|-------------|---------|--------------|
| `GEMINI_API_KEY` | Google Gemini API key | `AIza...` | https://makersuite.google.com/app/apikey |
| `SUPABASE_URL` | Supabase project URL | `https://xxx.supabase.co` | Supabase Dashboard → Settings → API |
| `SUPABASE_KEY` | Supabase anon key | `eyJh...` | Supabase Dashboard → Settings → API |
| `JWT_SECRET_KEY` | Secret for JWT tokens | Random 32+ chars | Generate with `secrets.token_urlsafe(32)` |

### Optional Variables

| Variable | Description | Default | Notes |
|----------|-------------|---------|-------|
| `JWT_ALGORITHM` | JWT algorithm | `HS256` | Don't change unless needed |
| `JWT_EXPIRATION_MINUTES` | Token expiration | `10080` (7 days) | In minutes |
| `DATABASE_URL` | PostgreSQL URL | From Supabase | Auto-constructed |
| `PORT` | Server port | `8080` | Railway sets automatically |

### Getting API Keys

**1. Google Gemini API Key:**
```
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Select project or create new
4. Copy the key (starts with AIza...)
5. Add to Railway environment variables
```

**2. Supabase Credentials:**
```
1. Go to https://supabase.com
2. Create new project or select existing
3. Go to Settings → API
4. Copy "Project URL" (SUPABASE_URL)
5. Copy "anon public" key (SUPABASE_KEY)
6. Add both to Railway environment variables
```

**3. JWT Secret Key:**
```bash
# Generate secure random key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use OpenSSL
openssl rand -base64 32
```

---

## Docker Configuration

### Dockerfile Explanation

**File:** `backend/Dockerfile`

```dockerfile
# Stage 1: Builder - Install dependencies
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Minimal production image
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Create directories for ChromaDB and medical knowledge
RUN mkdir -p /app/chroma_db /app/data/medical_knowledge && \
    chmod -R 755 /app/chroma_db /app/data/medical_knowledge

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD ["sh", "-c", "curl -f http://localhost:${PORT:-8080}/health || exit 1"]

# Run application
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"]
```

### Multi-Stage Build Benefits

1. **Smaller Image Size**: ~2GB vs 4GB+ (single-stage)
2. **Faster Deployments**: Less data to transfer
3. **Better Security**: No build tools in production
4. **CPU-Only PyTorch**: Optimized for Railway (no GPU)

### .dockerignore

**File:** `backend/.dockerignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
chroma_db/
*.db
*.sqlite3
.env
.env.local

# Git
.git/
.gitignore
```

---

## Database Setup

### Supabase Configuration

**1. Create Supabase Project:**
```
1. Go to https://supabase.com
2. Click "New Project"
3. Enter project details
4. Wait for provisioning (~2 minutes)
```

**2. Database Tables:**

Tables are auto-created on first run via SQLAlchemy:

```python
# backend/app/models/database.py

class User(Base):
    __tablename__ = "users"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID, ForeignKey("conversations.id"))
    role = Column(String)  # 'user' or 'assistant'
    content = Column(Text)
    agent_used = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**3. Verify Tables:**
```
1. Go to Supabase Dashboard
2. Click "Table Editor"
3. Should see: users, conversations, messages
```

### ChromaDB Setup

**Persistent Storage:**
- ChromaDB data stored in `/app/chroma_db`
- Mounted as Railway volume
- Survives deployments
- Auto-created on first run

**Initialize Medical Knowledge:**
```python
# Run once to populate vector store
python backend/scripts/populate_medical_knowledge.py
```

---

## Monitoring & Maintenance

### Health Checks

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

**Railway Auto-Monitoring:**
- Health checks every 30 seconds
- Auto-restart on failure
- Alerts on repeated failures

### Logging

**View Logs:**
```
Railway Dashboard → Deployments → Select deployment → Deploy Logs
```

**Log Levels:**
- `INFO`: Normal operations
- `WARNING`: Rate limits, retries
- `ERROR`: Failures, exceptions

**Key Log Messages:**
```
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8080
INFO: [SymptomAnalyzer] Processing query: ...
ERROR: RAG retrieval failed: ...
```

### Performance Metrics

**Railway Dashboard → Metrics:**
- CPU usage
- Memory usage
- Network traffic
- Request count
- Response times

**Optimization Tips:**
- Keep memory < 1GB
- CPU spikes normal during LLM calls
- Monitor request rate vs rate limit

### Scaling

**Horizontal Scaling:**
```
Railway Dashboard → Settings → Replicas
- Increase replicas for high traffic
- Load balancing automatic
- Stateless design supports scaling
```

**Vertical Scaling:**
```
Railway Dashboard → Settings → Resources
- Increase vCPU (default: 2)
- Increase memory (default: 1GB)
- Upgrade plan if needed
```

---

## Troubleshooting

### Common Issues

#### 1. "Invalid value for '--port': '$PORT' is not a valid integer"

**Cause:** PORT variable not expanded in CMD

**Fix:**
```dockerfile
# Wrong:
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}

# Correct:
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"]
```

Or set custom start command in Railway Dashboard.

#### 2. "Application failed to respond" (502 Error)

**Causes:**
- App crashed on startup
- Environment variables missing
- Database connection failed

**Debug:**
```
1. Check Deploy Logs for errors
2. Verify all environment variables set
3. Test Supabase connection
4. Check health endpoint
```

#### 3. ChromaDB "Permission Denied"

**Cause:** Volume mount permissions

**Fix:**
```dockerfile
RUN mkdir -p /app/chroma_db && \
    chmod -R 755 /app/chroma_db
```

#### 4. "Rate limit exceeded"

**Cause:** Too many requests from single IP

**Fix:**
- Increase rate limit in `app/middleware/rate_limit.py`
- Or implement user-based rate limiting
- Current: 100 requests/minute per IP

#### 5. Gemini API "Quota exceeded"

**Cause:** Free tier limits reached

**Fix:**
- Upgrade Gemini API plan
- Implement request caching
- Reduce LLM calls

### Debug Checklist

**Backend not starting:**
- [ ] Check Deploy Logs for errors
- [ ] Verify all environment variables set
- [ ] Test database connection
- [ ] Check Dockerfile syntax
- [ ] Verify requirements.txt has all dependencies

**Frontend can't connect:**
- [ ] Verify API URL in `api_constants.dart`
- [ ] Check CORS settings in backend
- [ ] Test backend health endpoint
- [ ] Check network connectivity
- [ ] Verify JWT token generation

**Agents not responding:**
- [ ] Check Gemini API key valid
- [ ] Verify ChromaDB initialized
- [ ] Check agent logs
- [ ] Test RAG retrieval
- [ ] Verify LangGraph workflow

### Support Resources

- **Railway Docs**: https://docs.railway.app
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **LangGraph Docs**: https://langchain-ai.github.io/langgraph
- **Supabase Docs**: https://supabase.com/docs
- **GitHub Issues**: https://github.com/BeamlakTamirat/Dr-Heal-Ai/issues

---

## Continuous Deployment

### Auto-Deploy on Git Push

**Railway automatically deploys when you push to GitHub:**

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Railway will:
# 1. Detect push
# 2. Build Docker image
# 3. Run tests (if configured)
# 4. Deploy new version
# 5. Health check
# 6. Switch traffic to new deployment
```

### Rollback

**If deployment fails:**
```
1. Go to Railway Dashboard → Deployments
2. Find last working deployment
3. Click "Redeploy"
4. Traffic switches back immediately
```

---

## Production Checklist

Before going live:

- [ ] All environment variables set
- [ ] Supabase database configured
- [ ] ChromaDB volume mounted
- [ ] Health checks passing
- [ ] API documentation accessible
- [ ] Rate limiting configured
- [ ] Logging enabled
- [ ] Error handling tested
- [ ] Security headers configured
- [ ] CORS properly set
- [ ] SSL/TLS enabled (automatic on Railway)
- [ ] Custom domain configured (optional)
- [ ] Monitoring alerts set up
- [ ] Backup strategy defined

---

**Your Dr.Heal AI backend is now production-ready on Railway! 🚀**
