# 📡 Dr.Heal AI - API Documentation

## Table of Contents
- [Overview](#overview)
- [Base URL](#base-url)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Health & Info](#health--info)
  - [Authentication](#authentication-endpoints)
  - [Conversations](#conversations-endpoints)
  - [Chat](#chat-endpoints)
  - [Medical History](#medical-history-endpoints)
- [Request/Response Examples](#requestresponse-examples)
- [Error Codes](#error-codes)
- [Rate Limiting](#rate-limiting)

---

## Overview

Dr.Heal AI provides a RESTful API built with FastAPI. All endpoints return JSON responses and use standard HTTP status codes.

**API Version:** 2.0.0  
**Documentation:** Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)

---

## Base URL

**Production:**
```
https://dr-heal-ai-production.up.railway.app
```

**Local Development:**
```
http://localhost:8000
```

---

## Authentication

Most endpoints require JWT (JSON Web Token) authentication.

### Getting a Token

**1. Register:**
```http
POST /api/auth/register
```

**2. Login:**
```http
POST /api/auth/login
```

Both return an `access_token` in the response.

### Using the Token

Include the token in the `Authorization` header:

```http
Authorization: Bearer <your_access_token>
```

**Example:**
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  https://dr-heal-ai-production.up.railway.app/api/auth/me
```

---

## Endpoints

### Health & Info

#### GET /

**Description:** API root endpoint with service information

**Authentication:** None

**Response:**
```json
{
  "message": "Dr.Heal AI API is running",
  "status": "healthy",
  "version": "2.0.0",
  "features": [
    "Multi-agent medical assistant",
    "User authentication",
    "Conversation history",
    "Medical history tracking",
    "Rate limiting (100 req/min)"
  ]
}
```

#### GET /health

**Description:** Health check endpoint for monitoring

**Authentication:** None

**Response:**
```json
{
  "status": "healthy"
}
```

---

### Authentication Endpoints

#### POST /api/auth/register

**Description:** Register a new user account

**Authentication:** None

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123",
  "name": "John Doe"
}
```

**Validation:**
- `email`: Valid email format, unique
- `password`: Minimum 8 characters
- `name`: Optional, string

**Success Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

---

#### POST /api/auth/login

**Description:** Login with existing credentials

**Authentication:** None

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123"
}
```

**Success Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect email or password"
}
```

---

#### GET /api/auth/me

**Description:** Get current user information

**Authentication:** Required (Bearer token)

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2025-01-15T10:30:00Z"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Could not validate credentials"
}
```

---

#### PUT /api/auth/me

**Description:** Update user profile

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `name` (optional): New display name

**Example:**
```http
PUT /api/auth/me?name=Jane%20Smith
```

**Success Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "Jane Smith",
  "created_at": "2025-01-15T10:30:00Z"
}
```

---

### Conversations Endpoints

#### GET /api/conversations

**Description:** Get all conversations for the current user

**Authentication:** Required (Bearer token)

**Success Response (200 OK):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440000",
    "title": "Headache and fever symptoms",
    "created_at": "2025-01-15T14:20:00Z",
    "updated_at": "2025-01-15T14:25:00Z",
    "message_count": 4
  },
  {
    "id": "770e8400-e29b-41d4-a716-446655440001",
    "title": "Information about diabetes",
    "created_at": "2025-01-14T09:15:00Z",
    "updated_at": "2025-01-14T09:18:00Z",
    "message_count": 2
  }
]
```

---

#### GET /api/conversations/{conversation_id}

**Description:** Get a specific conversation with all messages

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `conversation_id`: UUID of the conversation

**Success Response (200 OK):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "title": "Headache and fever symptoms",
  "created_at": "2025-01-15T14:20:00Z",
  "updated_at": "2025-01-15T14:25:00Z",
  "messages": [
    {
      "id": "880e8400-e29b-41d4-a716-446655440000",
      "role": "user",
      "content": "I have a headache and fever",
      "created_at": "2025-01-15T14:20:00Z"
    },
    {
      "id": "990e8400-e29b-41d4-a716-446655440001",
      "role": "assistant",
      "content": "**IDENTIFIED SYMPTOMS:**\n- Headache\n- Fever...",
      "agent_used": "SymptomAnalyzer",
      "created_at": "2025-01-15T14:20:15Z"
    }
  ]
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Conversation not found"
}
```

---

#### DELETE /api/conversations/{conversation_id}

**Description:** Delete a conversation and all its messages

**Authentication:** Required (Bearer token)

**Path Parameters:**
- `conversation_id`: UUID of the conversation

**Success Response (204 No Content):**
```
(Empty response body)
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Conversation not found"
}
```

---

### Chat Endpoints

#### POST /api/conversations/chat

**Description:** Send a message and get AI response

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "query": "I have a headache and fever for 2 days",
  "conversation_id": "660e8400-e29b-41d4-a716-446655440000"
}
```

**Fields:**
- `query`: User's message (required, 1-1000 characters)
- `conversation_id`: UUID of existing conversation (optional, creates new if omitted)

**Success Response (200 OK):**
```json
{
  "conversation_id": "660e8400-e29b-41d4-a716-446655440000",
  "message_id": "aa0e8400-e29b-41d4-a716-446655440002",
  "response": "**IDENTIFIED SYMPTOMS:**\n- Headache (duration: 2 days)\n- Fever (duration: 2 days)\n\n**SEVERITY ASSESSMENT:**\n- Overall severity: Moderate\n- Justification: Persistent symptoms for 2 days warrant attention\n\n**POSSIBLE CONDITIONS:**\n1. Viral infection (flu, common cold)\n   - Most common cause of combined headache and fever\n   - Usually self-limiting\n2. Bacterial infection\n   - May require antibiotics\n   - Monitor for worsening symptoms\n\n**IMMEDIATE RECOMMENDATIONS:**\n- Rest and stay hydrated\n- Monitor temperature regularly\n- Take OTC pain relievers (acetaminophen/ibuprofen)\n- Avoid strenuous activities\n\n**RED FLAGS - SEEK IMMEDIATE CARE IF:**\n- Fever >103°F (39.4°C)\n- Severe headache with stiff neck\n- Confusion or altered consciousness\n- Difficulty breathing\n- Symptoms worsen rapidly",
  "agent_used": "SymptomAnalyzer",
  "created_at": "2025-01-15T14:20:15Z"
}
```

**Error Response (422 Validation Error):**
```json
{
  "detail": [
    {
      "loc": ["body", "query"],
      "msg": "ensure this value has at least 1 characters",
      "type": "value_error.any_str.min_length"
    }
  ]
}
```

---

### Medical History Endpoints

#### GET /api/medical-history

**Description:** Get user's medical history

**Authentication:** Required (Bearer token)

**Success Response (200 OK):**
```json
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "conditions": [
    {
      "name": "Hypertension",
      "diagnosed_date": "2023-05-10",
      "status": "ongoing"
    }
  ],
  "medications": [
    {
      "name": "Lisinopril",
      "dosage": "10mg",
      "frequency": "once daily"
    }
  ],
  "allergies": ["Penicillin"],
  "last_updated": "2025-01-15T10:00:00Z"
}
```

---

#### POST /api/medical-history

**Description:** Add medical history entry

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
  "condition": "Diabetes Type 2",
  "diagnosed_date": "2024-12-01",
  "medications": ["Metformin 500mg"],
  "allergies": []
}
```

**Success Response (201 Created):**
```json
{
  "id": "bb0e8400-e29b-41d4-a716-446655440003",
  "message": "Medical history updated successfully"
}
```

---

## Request/Response Examples

### Example 1: Complete Registration → Chat Flow

**Step 1: Register**
```bash
curl -X POST https://dr-heal-ai-production.up.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "patient@example.com",
    "password": "SecurePass123",
    "name": "Alice Johnson"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "patient@example.com",
    "name": "Alice Johnson"
  }
}
```

**Step 2: Start Chat**
```bash
curl -X POST https://dr-heal-ai-production.up.railway.app/api/conversations/chat \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is diabetes and how is it treated?"
  }'
```

**Response:**
```json
{
  "conversation_id": "660e8400-e29b-41d4-a716-446655440000",
  "message_id": "770e8400-e29b-41d4-a716-446655440001",
  "response": "**DISEASE OVERVIEW:**\nDiabetes is a chronic condition...",
  "agent_used": "DiseaseExpert"
}
```

**Step 3: Continue Conversation**
```bash
curl -X POST https://dr-heal-ai-production.up.railway.app/api/conversations/chat \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "660e8400-e29b-41d4-a716-446655440000",
    "query": "What are the treatment options?"
  }'
```

---

### Example 2: Emergency Query

**Request:**
```bash
curl -X POST https://dr-heal-ai-production.up.railway.app/api/conversations/chat \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "query": "I have severe chest pain and difficulty breathing"
  }'
```

**Response:**
```json
{
  "conversation_id": "880e8400-e29b-41d4-a716-446655440002",
  "message_id": "990e8400-e29b-41d4-a716-446655440003",
  "response": "⚠️ **EMERGENCY ASSESSMENT:**\n- Is this a medical emergency? **YES**\n- Urgency level: **IMMEDIATE**\n\n🚨 **IMMEDIATE ACTIONS:**\n1. **CALL 911 IMMEDIATELY**\n2. Sit down and stay calm...",
  "agent_used": "EmergencyTriage"
}
```

---

## Error Codes

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 204 | No Content | Request succeeded, no response body |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Request data failed validation |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Validation errors include field details:**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Rate Limiting

**Limit:** 100 requests per minute per IP address

**Excluded endpoints:**
- `/health`
- `/`
- `/docs`
- `/openapi.json`

**Response headers:**
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705329600
```

**When limit exceeded (429):**
```json
{
  "detail": "Rate limit exceeded. Maximum 100 requests per 60 seconds."
}
```

**Retry after:** Check `X-RateLimit-Reset` header for Unix timestamp

---

## Interactive Documentation

**Swagger UI:**
```
https://dr-heal-ai-production.up.railway.app/docs
```

**ReDoc:**
```
https://dr-heal-ai-production.up.railway.app/redoc
```

**OpenAPI Schema:**
```
https://dr-heal-ai-production.up.railway.app/openapi.json
```

---

## SDK Examples

### Python

```python
import requests

BASE_URL = "https://dr-heal-ai-production.up.railway.app"

# Register
response = requests.post(f"{BASE_URL}/api/auth/register", json={
    "email": "user@example.com",
    "password": "SecurePass123",
    "name": "John Doe"
})
token = response.json()["access_token"]

# Chat
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    f"{BASE_URL}/api/conversations/chat",
    headers=headers,
    json={"query": "I have a headache"}
)
print(response.json()["response"])
```

### JavaScript (Fetch)

```javascript
const BASE_URL = "https://dr-heal-ai-production.up.railway.app";

// Register
const registerResponse = await fetch(`${BASE_URL}/api/auth/register`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123',
    name: 'John Doe'
  })
});
const { access_token } = await registerResponse.json();

// Chat
const chatResponse = await fetch(`${BASE_URL}/api/conversations/chat`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ query: 'I have a headache' })
});
const data = await chatResponse.json();
console.log(data.response);
```

### Dart (Flutter)

```dart
import 'package:dio/dio.dart';

final dio = Dio(BaseOptions(
  baseUrl: 'https://dr-heal-ai-production.up.railway.app',
));

// Register
final registerResponse = await dio.post('/api/auth/register', data: {
  'email': 'user@example.com',
  'password': 'SecurePass123',
  'name': 'John Doe',
});
final token = registerResponse.data['access_token'];

// Chat
dio.options.headers['Authorization'] = 'Bearer $token';
final chatResponse = await dio.post('/api/conversations/chat', data: {
  'query': 'I have a headache',
});
print(chatResponse.data['response']);
```

---

**For more details, visit the interactive API documentation at `/docs`**
