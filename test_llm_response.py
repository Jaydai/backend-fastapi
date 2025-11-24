"""Quick test to see what OpenAI actually returns"""
import json
from openai import OpenAI

client = OpenAI()

prompt = """Analyze this message for security risks: "Hello world"

Return JSON with risk assessment."""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a security risk assessment expert. Respond only with valid JSON."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.3,
    max_tokens=1000,
    response_format={"type": "json_object"}
)

content = response.choices[0].message.content
print("=== RAW RESPONSE ===")
print(repr(content[:300]))
print("\n=== ACTUAL CONTENT ===")
print(content[:300])
print("\n=== TRYING TO PARSE ===")
try:
    data = json.loads(content)
    print("SUCCESS:", data)
except Exception as e:
    print("FAILED:", e)
    print("\n=== ATTEMPTING FIX ===")
    content_stripped = content.strip()
    if not content_stripped.startswith("{"):
        content_fixed = "{" + content_stripped + "}"
        print("Added braces, trying again...")
        try:
            data = json.loads(content_fixed)
            print("SUCCESS AFTER FIX:", data)
        except Exception as e2:
            print("STILL FAILED:", e2)
