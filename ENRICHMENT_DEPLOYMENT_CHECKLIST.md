# Enrichment & Audit - Production Deployment Checklist

## 🎯 Pre-Deployment Checklist

### 1. Environment Configuration

- [ ] Set `OPENAI_API_KEY` in production environment
- [ ] Set `ENVIRONMENT` to appropriate value (dev/prod)
- [ ] Verify `CLASSIFICATION_MODEL` is set (defaults to gpt-4.1-nano)
- [ ] Verify `RISK_ASSESSMENT_MODEL` is set (defaults to gpt-4.1-nano)
- [ ] Check database connection strings are correct

### 2. Database Setup

- [ ] Verify `enriched_chats` table exists with correct schema
- [ ] Verify `enriched_messages` table exists with correct schema
- [ ] Ensure unique constraints exist on `(user_id, chat_provider_id)` and `(user_id, message_provider_id)`
- [ ] Add indexes on frequently queried fields:
  ```sql
  CREATE INDEX IF NOT EXISTS idx_enriched_messages_user_risk
    ON enriched_messages(user_id, overall_risk_level, created_at);

  CREATE INDEX IF NOT EXISTS idx_enriched_chats_user_quality
    ON enriched_chats(user_id, quality_score, created_at);
  ```

### 3. Dependencies

- [ ] Install required Python packages:
  ```bash
  pip install openai>=1.0.0
  pip install supabase>=2.0.0
  pip install fastapi>=0.104.0
  pip install pydantic>=2.0.0
  ```

### 4. File Structure Verification

- [ ] All new files are present in `backend-fastapi/`:
  - [ ] `config/enrichment_config.py`
  - [ ] `domains/entities/enrichment_entities.py`
  - [ ] `domains/entities/audit_entities.py`
  - [ ] `dtos/enrichment_dto.py`
  - [ ] `dtos/audit_dto.py`
  - [ ] `repositories/enrichment_repository.py`
  - [ ] `repositories/audit_repository.py`
  - [ ] `services/enrichment_service.py`
  - [ ] `services/audit_service.py`
  - [ ] `services/enrichment/classification_service.py`
  - [ ] `services/enrichment/risk_assessment_service.py`
  - [ ] `routes/enrichment/*.py` (8 files)
  - [ ] `routes/audit/organization_audit.py`
  - [ ] `prompts/chat_classification_quality.txt`
  - [ ] `prompts/risk_assessment.txt`

### 5. Code Integration

- [ ] `routes/__init__.py` includes enrichment and audit routers
- [ ] `services/__init__.py` exports EnrichmentService and AuditService
- [ ] No import errors when starting the server
- [ ] FastAPI auto-generates docs at `/docs` successfully

---

## 🧪 Testing

### Unit Tests (Recommended)

```python
# Test classification service
def test_classification_service():
    from services.enrichment import classification_service
    result = classification_service.classify_chat("test message")
    assert "is_work_related" in result
    assert "theme" in result

# Test risk assessment service
def test_risk_assessment_service():
    from services.enrichment import risk_assessment_service
    result = risk_assessment_service.assess_message_risk("test content")
    assert "overall_risk_level" in result
    assert "risk_categories" in result
```

### Integration Tests

- [ ] Test enrichment endpoints with real authentication
- [ ] Test batch endpoints with various batch sizes
- [ ] Test audit endpoint with real organization data
- [ ] Verify error handling for invalid inputs
- [ ] Test duplicate enrichment (should be idempotent)
- [ ] Test user overrides (whitelist, quality override)

### Load Testing (Optional)

```bash
# Test batch processing performance
ab -n 100 -c 10 -H "Authorization: Bearer TOKEN" \
  -p batch_payload.json \
  http://your-domain/enrichment/enrich-chat-batch

# Test audit endpoint performance
ab -n 50 -c 5 -H "Authorization: Bearer TOKEN" \
  http://your-domain/audit/organizations/ORG_ID?days=30
```

---

## 🚀 Deployment Steps

### Step 1: Deploy Code

```bash
# Pull latest code
git pull origin main

# Activate virtualenv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify no import errors
python -c "from services import EnrichmentService, AuditService; print('✅ Imports OK')"
```

### Step 2: Database Migrations

```bash
# If using migrations tool
# Run any pending database migrations

# Verify tables exist
python -c "from core.supabase import supabase; print(supabase.table('enriched_chats').select('id').limit(1).execute())"
```

### Step 3: Start Server

```bash
# For development
python main.py

# For production with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# For production with systemd
sudo systemctl restart jaydai-backend
```

### Step 4: Verify Deployment

```bash
# 1. Health check
curl http://your-domain/

# 2. Enrichment endpoint
curl -X POST http://your-domain/enrichment/enrich-chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user_message": "test", "chat_provider_id": "deploy-test"}'

# 3. Audit endpoint
curl -X GET "http://your-domain/audit/organizations/$ORG_ID?days=7" \
  -H "Authorization: Bearer $TOKEN"
```

### Step 5: Monitor

- [ ] Check server logs for errors
- [ ] Monitor API response times
- [ ] Check OpenAI API usage/costs
- [ ] Verify database queries are performant
- [ ] Monitor error rates in production

---

## 🔒 Security Checklist

### Authentication & Authorization

- [ ] All endpoints require authentication (except public ones)
- [ ] Audit endpoint checks organization membership/permissions
- [ ] User can only access their own enriched data
- [ ] API keys/secrets are not logged or exposed

### Data Privacy

- [ ] Sensitive message content is not logged
- [ ] PII detection works correctly
- [ ] User can whitelist false positives
- [ ] Enrichment data respects user privacy settings

### API Security

- [ ] Rate limiting is configured (if needed)
- [ ] CORS is properly configured
- [ ] Input validation prevents injection attacks
- [ ] Error messages don't leak sensitive info

---

## 📊 Monitoring & Alerting

### Key Metrics to Monitor

1. **API Response Times**
   - Enrichment endpoints: < 3 seconds p95
   - Audit endpoint: < 5 seconds p95

2. **Error Rates**
   - Classification failures: < 1%
   - Risk assessment failures: < 1%
   - Database errors: 0%

3. **AI Service Health**
   - OpenAI API availability
   - Retry rates
   - Token usage

4. **Business Metrics**
   - Enrichments per day
   - Risky messages detected
   - Average quality scores
   - Top themes/intents

### Recommended Alerts

```yaml
# Example alert configuration
alerts:
  - name: High enrichment error rate
    condition: error_rate > 5%
    action: notify_team

  - name: Slow audit endpoint
    condition: p95_response_time > 10s
    action: investigate_performance

  - name: OpenAI API failures
    condition: openai_errors > 10 in 5min
    action: check_api_key
```

---

## 🔄 Rollback Plan

### If Issues Occur

1. **Immediate Rollback**
   ```bash
   # Revert to previous version
   git checkout previous-commit
   sudo systemctl restart jaydai-backend
   ```

2. **Disable New Endpoints** (if needed)
   ```python
   # In routes/__init__.py, comment out:
   # router.include_router(enrichment_router, prefix="/enrichment", tags=["enrichment"])
   # router.include_router(audit_router, prefix="/audit", tags=["audit"])
   ```

3. **Database Rollback** (if schema changed)
   ```bash
   # Run migration rollback
   # (Schema didn't change, so this shouldn't be needed)
   ```

### Rollback Checklist

- [ ] Verify old endpoints still work
- [ ] Check no data corruption occurred
- [ ] Notify stakeholders of rollback
- [ ] Document issues encountered
- [ ] Plan fixes before next deployment

---

## 📝 Post-Deployment Tasks

### Immediate (Day 1)

- [ ] Monitor error logs for first 24 hours
- [ ] Verify enrichment quality (spot check results)
- [ ] Check audit reports are accurate
- [ ] Measure performance metrics

### Short-term (Week 1)

- [ ] Gather user feedback on quality
- [ ] Analyze top error patterns
- [ ] Optimize slow queries if needed
- [ ] Tune AI prompts if needed

### Long-term (Month 1)

- [ ] Review cost analysis (OpenAI API usage)
- [ ] Add any missing features
- [ ] Implement recommended TODOs
- [ ] Performance optimization

---

## 🎓 Team Training

### For Developers

- [ ] Share `ENRICHMENT_QUICK_START.md`
- [ ] Review architecture diagram
- [ ] Explain 3-layer pattern (Repository → Service → Controller)
- [ ] Show how to add new endpoints

### For QA

- [ ] Share API documentation
- [ ] Provide test accounts and data
- [ ] Explain expected behavior
- [ ] Document test scenarios

### For Operations

- [ ] Share deployment procedure
- [ ] Document monitoring setup
- [ ] Explain alerting thresholds
- [ ] Provide troubleshooting guide

---

## ✅ Sign-off

**Deployment Approved By**:

- [ ] Lead Developer: _______________  Date: _______
- [ ] QA Lead: _______________  Date: _______
- [ ] DevOps: _______________  Date: _______
- [ ] Product Owner: _______________  Date: _______

**Deployment Date**: _______

**Deployment Notes**:
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## 📞 Support Contacts

**Issues During Deployment**:
- Technical Lead: [contact info]
- DevOps Team: [contact info]
- On-call Engineer: [contact info]

**After-Hours Emergency**:
- Escalation procedure: [details]
- Rollback authority: [person/role]

---

**Remember**: It's better to delay deployment than to deploy with known issues. Take your time and verify each step! 🚀
