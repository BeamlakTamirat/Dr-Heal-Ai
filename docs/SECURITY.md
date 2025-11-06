# 🔒 Dr.Heal AI - Security Documentation

## Table of Contents
- [Overview](#overview)
- [Authentication & Authorization](#authentication--authorization)
- [Input Validation](#input-validation)
- [Rate Limiting](#rate-limiting)
- [Data Protection](#data-protection)
- [API Security](#api-security)
- [Security Best Practices](#security-best-practices)

---

## Overview

Dr.Heal AI implements enterprise-grade security measures to protect user data and ensure safe operation.

**Security Features:**
- JWT authentication with bcrypt password hashing
- Rate limiting (100 requests/minute)
- Input validation and sanitization
- CORS configuration
- Secure API key management
- SQL injection prevention
- XSS protection

---

## Authentication & Authorization

### JWT (JSON Web Tokens)

**Implementation:** `backend/app/auth/security.py`

**Token Generation:**
```python
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=10080)  # 7 days
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt
```

**Token Validation:**
```python
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Configuration:**
- Algorithm: HS256
- Expiration: 7 days (10080 minutes)
- Secret Key: Environment variable (never hardcoded)

### Password Hashing

**Library:** bcrypt via passlib

**Implementation:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Security Features:**
- Bcrypt with automatic salt generation
- Configurable work factor (default: 12 rounds)
- Resistant to rainbow table attacks
- Slow by design (prevents brute force)

### Protected Endpoints

**Dependency Injection:**
```python
from fastapi import Depends
from app.auth.security import get_current_user

@app.get("/api/auth/me")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user
```

**All protected endpoints:**
- `/api/auth/me` - User profile
- `/api/conversations/*` - Conversation management
- `/api/medical-history/*` - Medical records

---

## Input Validation

### Pydantic Models

**Request Validation:**
```python
from pydantic import BaseModel, EmailStr, constr

class RegisterRequest(BaseModel):
    email: EmailStr  # Validates email format
    password: constr(min_length=8)  # Minimum 8 characters
    name: str

class ChatRequest(BaseModel):
    query: constr(min_length=1, max_length=1000)  # 1-1000 chars
    conversation_id: Optional[UUID] = None
```

**Validation Rules:**
- Email: Valid format, RFC 5322 compliant
- Password: Minimum 8 characters
- Query: 1-1000 characters
- UUIDs: Valid UUID4 format

### SQL Injection Prevention

**ORM Usage:**
```python
# Safe - SQLAlchemy ORM
user = db.query(User).filter(User.email == email).first()

# Unsafe - Raw SQL (NOT USED)
# db.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

**All database queries use SQLAlchemy ORM**, preventing SQL injection.

### XSS Protection

**Content-Type Headers:**
```python
response.headers["Content-Type"] = "application/json"
```

**No HTML rendering** - API returns only JSON, preventing XSS attacks.

---

## Rate Limiting

### Implementation

**File:** `backend/app/middleware/rate_limit.py`

**Configuration:**
- Limit: 100 requests per 60 seconds
- Scope: Per IP address
- Excluded: `/health`, `/`, `/docs`

**Middleware:**
```python
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.clients: Dict[str, list] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        
        # Clean old timestamps
        self.clients[client_ip] = [
            ts for ts in self.clients[client_ip]
            if now - ts < self.period
        ]
        
        # Check limit
        if len(self.clients[client_ip]) >= self.calls:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        self.clients[client_ip].append(now)
        return await call_next(request)
```

**Response Headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705329600
```

---

## Data Protection

### Environment Variables

**Secure Storage:**
```bash
# .env file (NEVER commit to git)
GEMINI_API_KEY=AIza...
SUPABASE_URL=https://...
SUPABASE_KEY=eyJh...
JWT_SECRET_KEY=random_secret_key
```

**Loading:**
```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
```

**.gitignore:**
```
.env
.env.local
*.key
*.pem
```

### Database Security

**Connection Security:**
- SSL/TLS encryption (Supabase)
- Connection pooling
- Prepared statements (SQLAlchemy)

**Data Encryption:**
- Passwords: bcrypt hashed
- Tokens: JWT signed
- API keys: Environment variables

### CORS Configuration

**File:** `backend/app/main.py`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production: Specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Production Recommendation:**
```python
allow_origins=[
    "https://your-frontend-domain.com",
    "https://dr-heal-ai.app"
]
```

---

## API Security

### HTTPS Only

**Production:**
- Railway provides automatic SSL/TLS
- All traffic encrypted
- HSTS headers enabled

**Certificate:**
- Auto-renewed by Railway
- Let's Encrypt certificates
- TLS 1.2+ only

### API Key Management

**Gemini API Key:**
- Stored in environment variable
- Never logged or exposed
- Rotated regularly

**Best Practices:**
```python
# Good - Environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Bad - Hardcoded (NEVER DO THIS)
# GEMINI_API_KEY = "AIzaSyD..."
```

### Error Handling

**Safe Error Messages:**
```python
try:
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
except Exception as e:
    logger.error(f"Authentication error: {e}")
    raise HTTPException(status_code=401, detail="Authentication failed")
```

**Never expose:**
- Stack traces to users
- Database errors
- Internal paths
- API keys in logs

---

## Security Best Practices

### Implemented Measures

✅ **Authentication:**
- JWT tokens with expiration
- Bcrypt password hashing
- Secure token storage

✅ **Authorization:**
- User-scoped data access
- Protected endpoints
- Token validation

✅ **Input Validation:**
- Pydantic models
- Type checking
- Length limits

✅ **Rate Limiting:**
- Per-IP throttling
- Configurable limits
- Graceful degradation

✅ **Data Protection:**
- Environment variables
- No secrets in code
- Encrypted connections

✅ **Error Handling:**
- Safe error messages
- Comprehensive logging
- Graceful failures

### Security Checklist

**Before Deployment:**
- [ ] All API keys in environment variables
- [ ] JWT secret key is random and secure
- [ ] CORS origins restricted to production domains
- [ ] Rate limiting enabled
- [ ] HTTPS enforced
- [ ] Error messages don't expose internals
- [ ] Logging doesn't include sensitive data
- [ ] Database uses SSL/TLS
- [ ] Password requirements enforced
- [ ] Input validation on all endpoints

### Monitoring & Alerts

**Log Security Events:**
```python
logger.warning(f"Failed login attempt for {email}")
logger.warning(f"Rate limit exceeded for {client_ip}")
logger.error(f"Invalid token: {token[:10]}...")
```

**Monitor:**
- Failed authentication attempts
- Rate limit violations
- Invalid token usage
- Unusual traffic patterns

---

## Vulnerability Management

### Dependencies

**Regular Updates:**
```bash
pip list --outdated
pip install --upgrade <package>
```

**Security Scanning:**
```bash
pip install safety
safety check
```

### Reporting Security Issues

**Contact:**
- Email: security@dr-heal-ai.com
- GitHub: Private security advisory
- Response time: 24-48 hours

**Please include:**
- Description of vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

---

## Compliance

### HIPAA Considerations

**Note:** Dr.Heal AI is an informational tool, not a medical device.

**Data Handling:**
- No PHI (Protected Health Information) stored
- Conversations are user-scoped
- Users can delete their data
- No sharing with third parties

### GDPR Compliance

**User Rights:**
- Right to access (GET /api/auth/me)
- Right to deletion (DELETE /api/conversations/{id})
- Right to data portability (JSON export)
- Consent for data processing

---

**Dr.Heal AI prioritizes security to protect user data and ensure safe medical consultations! 🔒**
