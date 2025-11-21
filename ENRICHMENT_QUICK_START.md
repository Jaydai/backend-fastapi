# Enrichment & Audit - Quick Start Guide

## 🚀 Getting Started

### 1. Prerequisites

```bash
# Ensure you have OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Optional: Override models
export CLASSIFICATION_MODEL="gpt-4.1-nano"
export RISK_ASSESSMENT_MODEL="gpt-4.1-nano"
```

### 2. Start the Server

```bash
cd backend-fastapi
source venv/bin/activate  # or your virtualenv
python main.py
```

### 3. Test Endpoints

Visit: `http://localhost:8000/docs` for interactive API documentation

---

## 📡 API Examples

### Enrich a Chat

```bash
curl -X POST http://localhost:8000/enrichment/enrich-chat \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "Write a Python script to analyze sales data",
    "chat_provider_id": "chat_123"
  }'
```

**Response**:
```json
{
  "is_work_related": true,
  "theme": "data_analysis",
  "intent": "coding/generation",
  "quality": {
    "quality_score": 75,
    "clarity": 4,
    "context": 3,
    "specificity": 4,
    "actionability": 4
  },
  "feedback": {
    "summary": "Clear request but could benefit from more context",
    "strengths": ["Clear objective", "Specific task"],
    "improvements": ["Add data format details", "Specify output requirements"]
  }
}
```

### Assess Message Risk

```bash
curl -X POST http://localhost:8000/enrichment/enrich-message \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Here is my API key: sk-abc123xyz456",
    "message_provider_id": "msg_789"
  }'
```

**Response**:
```json
{
  "overall_risk_level": "critical",
  "overall_risk_score": 95.5,
  "risk_categories": {
    "security": {
      "level": "critical",
      "score": 100,
      "detected": true,
      "details": "API key detected in message"
    },
    "pii": {"level": "none", "score": 0, "detected": false}
  },
  "risk_summary": ["Critical: API key detected"],
  "detected_issues": [
    {
      "category": "security",
      "severity": "critical",
      "description": "API key detected"
    }
  ]
}
```

### Get Organization Audit

```bash
curl -X GET "http://localhost:8000/audit/organizations/org_123?days=30" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Response**: Comprehensive audit with quality stats, risk stats, usage stats, top users, etc.

---

## 🔧 Common Use Cases

### 1. Real-time Chat Monitoring

```python
from services.enrichment_service import EnrichmentService
from dtos.enrichment_dto import ChatEnrichmentRequestDTO

# Enrich chat as user sends it
dto = ChatEnrichmentRequestDTO(
    user_message=message_content,
    chat_provider_id=chat_id
)
result = EnrichmentService.enrich_chat(client, user_id, dto)

# Check if work-related
if result.is_work_related:
    # Track work usage
    pass
```

### 2. Batch Processing Historical Data

```python
from services.enrichment_service import EnrichmentService
from dtos.enrichment_dto import ChatEnrichmentBatchRequestDTO

# Process 50 chats at once
batch_dto = ChatEnrichmentBatchRequestDTO(chats=[...])
results = await EnrichmentService.enrich_chat_batch(client, user_id, batch_dto.chats)

# Check results
for result in results:
    if result["success"]:
        print(f"Enriched: {result['chat_provider_id']}")
    else:
        print(f"Failed: {result['error']}")
```

### 3. Risk Monitoring Dashboard

```python
from services.enrichment_service import EnrichmentService

# Get risky messages from last 7 days
risky_messages = EnrichmentService.get_risky_messages(
    client, user_id, days=7, min_risk_level="high", limit=50
)

for msg in risky_messages:
    print(f"Risk: {msg.risk_level} | Score: {msg.risk_score}")
    print(f"Categories: {msg.risk_categories.keys()}")
```

### 4. Organization-wide Audit Report

```python
from services.audit_service import AuditService

# Generate comprehensive audit (async)
audit = await AuditService.get_organization_audit(
    client, user_id, org_id,
    start_date=None, end_date=None, days=30
)

print(f"Total prompts: {audit.usage_stats.total_prompts}")
print(f"Average quality: {audit.quality_stats.average_score}")
print(f"Critical risks: {audit.risk_stats.critical_count}")
```

---

## 🎯 Key Features

### Batch Processing

- **Chat enrichment**: 1-50 chats in parallel
- **Message enrichment**: 1-100 messages sequentially (to avoid rate limits)
- Partial failure handling (some succeed, some fail)

### User Overrides

- **Whitelist risky messages**: User says "this is safe"
- **Override quality scores**: User disagrees with AI assessment

### Duplicate Detection

- Enrichment is idempotent
- Duplicate chats/messages are skipped automatically
- Uses unique constraints on `(user_id, provider_id)`

### Performance

- Audit queries run in parallel (8+ queries at once)
- Typical audit generation: < 2 seconds for 30 days
- Retry logic for AI services (up to 2 retries)

---

## 🔍 Debugging

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check AI Service Status

```python
from services.enrichment import classification_service

try:
    result = classification_service.classify_chat("test message")
    print("✅ Classification service working")
except Exception as e:
    print(f"❌ Error: {e}")
```

### Inspect Database State

```python
from repositories.enrichment_repository import EnrichmentRepository

# Check if chat is already enriched
existing = EnrichmentRepository.get_enriched_chat(client, user_id, chat_provider_id)
if existing:
    print(f"Already enriched: {existing.theme} / {existing.intent}")
```

---

## 📊 Configuration

All configuration is in `config/enrichment_config.py`:

```python
# Change models
DEFAULT_CLASSIFICATION_MODEL = "gpt-4.1-nano"
DEFAULT_RISK_ASSESSMENT_MODEL = "gpt-4.1-nano"

# Adjust risk thresholds
RISK_LEVEL_THRESHOLDS = {
    "critical": 80.0,
    "high": 60.0,
    "medium": 40.0,
    "low": 20.0
}

# Change category weights
RISK_CATEGORY_WEIGHTS = {
    "security": 1.5,  # Increase to prioritize security risks
    "pii": 1.2,
    # ...
}

# Adjust batch limits
MAX_CHAT_BATCH_SIZE = 50
MAX_MESSAGE_BATCH_SIZE = 100
```

---

## 🐛 Common Errors

### `"Classification service failed: Invalid JSON response"`

- **Cause**: AI returned malformed JSON
- **Solution**: Service retries automatically. If persists, check prompt template

### `"Message already enriched, skipping save"`

- **Cause**: Duplicate enrichment attempt (this is normal behavior)
- **Solution**: No action needed, idempotency is working

### `"No members found for organization"`

- **Cause**: Organization has no members or wrong organization ID
- **Solution**: Verify organization_id and membership in `users_metadata`

### `"Failed to fetch user: Authentication required"`

- **Cause**: Missing or invalid authentication token
- **Solution**: Ensure `Authorization: Bearer TOKEN` header is included

---

## 📚 Additional Resources

- **Full Documentation**: See `ENRICHMENT_MIGRATION.md`
- **API Docs**: `http://localhost:8000/docs` (when server running)
- **Prompts**: Customize AI behavior in `prompts/` directory
- **Old Implementation**: Reference `fastapi-backend/routes/enrichment/` for comparison

---

## 🎓 Architecture Overview

```
User Request
    ↓
[Routes] ← Thin controllers (auth, validation)
    ↓
[Services] ← Business logic, orchestration
    ↓
[AI Services] ← Classification, Risk Assessment
    ↓
[Repositories] ← Database operations only
    ↓
Database
```

**Key Principle**: Each layer has a single responsibility. Repositories don't know about business logic. Services don't know about HTTP. Routes don't know about database queries.

---

## ✅ Quick Health Check

```bash
# 1. Server is running
curl http://localhost:8000

# 2. Authentication works
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/users/me

# 3. Enrichment works
curl -X POST http://localhost:8000/enrichment/enrich-chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_message": "test", "chat_provider_id": "test-123"}'

# 4. Audit works
curl -X GET "http://localhost:8000/audit/organizations/$ORG_ID?days=7" \
  -H "Authorization: Bearer $TOKEN"
```

All endpoints should return `200 OK` (or valid responses).

---

**Questions?** Check the main documentation or dive into the code. The architecture is clean and well-structured! 🚀
