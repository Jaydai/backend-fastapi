# Assistant Instructions

This folder contains the complete system instructions for the OpenAI Assistants used in the enrichment system.

## Files

### 1. `chat_classification_instructions.txt`
**Purpose:** Instructions for the chat classification assistant that evaluates prompt quality and categorizes chats.

**Used by:**
- Chat enrichment endpoints (`/enrichment/enrich-chat`, `/enrichment/enrich-chat-batch`)
- Classification service

**Key features:**
- Theme classification (coding, marketing, sales, etc.)
- Intent detection (information_lookup, drafting, coding, etc.)
- Skill level assessment (beginner → expert)
- Domain expertise detection (tech stack, specialties)
- Quality scoring (clarity, context, specificity, actionability, complexity)
- Personalized feedback generation
- Productivity indicators (complexity, collaboration signals, reusability)

**Output format:** JSON with quality metrics, classifications, and feedback

### 2. `message_risk_assessment_instructions.txt`
**Purpose:** Instructions for the message risk assessment assistant that detects security and compliance risks.

**Used by:**
- Message enrichment endpoints (`/enrichment/enrich-message`, `/enrichment/enrich-message-batch`)
- Risk assessment service

**Key features:**
- 6 risk categories: PII, Security, Confidential, Misinformation, Data Leakage, Compliance
- Context-aware detection (actual data vs references/examples)
- Confidence scoring for each detection
- Suggested redactions for sensitive data
- Overall risk assessment with weighted scoring
- Action recommendations (block, warn, review, allow)

**Output format:** JSON with risk assessments per category and overall risk

## How to Update

### Option 1: Update OpenAI Assistant via API

```python
from openai import OpenAI

client = OpenAI()

# Read the instructions file
with open("assistant_instructions/chat_classification_instructions.txt", "r") as f:
    instructions = f.read()

# Update the assistant
client.beta.assistants.update(
    assistant_id="asst_XXXXXXXXX",  # Your assistant ID
    instructions=instructions
)
```

### Option 2: Update via OpenAI Dashboard

1. Go to https://platform.openai.com/assistants
2. Select your assistant
3. Copy the contents of the instruction file
4. Paste into the "Instructions" field
5. Save

## Configuration

The assistant IDs are configured in your environment variables:

```bash
# In .env file
CHAT_ENRICHMENT_ASSISTANT_ID=asst_XXXXXXXXX  # For chat classification
MESSAGE_ENRICHMENT_ASSISTANT_ID=asst_YYYYYYYYY  # For risk assessment
```

These are read by `config/enrichment_config.py`:
- `CHAT_ENRICHMENT_ASSISTANT_ID` - Used by ClassificationService
- `MESSAGE_ENRICHMENT_ASSISTANT_ID` - Used by RiskAssessmentService

## Important Notes

### Data Types
Both instructions emphasize returning **integers only** for numeric scores:
- ✅ Good: `"risk_score": 85`
- ❌ Bad: `"risk_score": 85.5`

The backend validation layer automatically converts floats to integers as a safety measure, but the instructions now explicitly request integers.

### Response Format
Both assistants must return **pure JSON only** - no markdown code blocks, no explanatory text:
- ✅ Good: `{"theme": "coding", "intent": "debugging"}`
- ❌ Bad: ` ```json\n{"theme": "coding"}\n``` `

### Validation
The backend includes comprehensive validation in `utils/enrichment/validators.py`:
- Converts string confidence values to numbers
- Handles missing optional fields (domain_expertise, productivity_indicators)
- Clamps scores to valid ranges
- Converts floats to integers
- Handles complexity_score of 0 by converting to null

## Testing

Test the assistants using the enrichment endpoints:

```bash
# Test chat classification
curl -X POST http://localhost:8000/enrichment/enrich-chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "How do I implement JWT authentication in FastAPI?",
    "user_id": "test-user-123"
  }'

# Test risk assessment
curl -X POST http://localhost:8000/enrichment/enrich-message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "My API key is sk-abc123",
    "user_id": "test-user-123"
  }'
```

## Version History

- **v1.0** (2025-11-24): Initial version with comprehensive instructions
  - Added explicit integer-only requirements for numeric scores
  - Enhanced examples and guidance
  - Clarified detection rules and context awareness
