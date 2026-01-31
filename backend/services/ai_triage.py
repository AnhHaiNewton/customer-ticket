import json
from google import genai
from google.genai import types
from schemas.ticket import AITriageResult
from env import env

client = genai.Client(api_key=env.GEMINI_API_KEY)

TRIAGE_PROMPT = """You are a customer support AI assistant. Analyze the following support ticket and provide a triage assessment.

Customer Name: {customer_name}
Subject: {subject}
Message: {message}

Respond ONLY with valid JSON in this exact format, no markdown, no explanation:
{{
    "category": "billing" | "technical" | "feature_request",
    "sentiment_score": <integer 1-10, where 1=very angry, 10=very happy>,
    "urgency": "high" | "medium" | "low",
    "draft_response": "<polite, helpful response to the customer>"
}}

Rules:
- category: "billing" for payment/subscription issues, "technical" for bugs/errors, "feature_request" for suggestions
- urgency: "high" if customer is angry or issue is blocking, "medium" for normal issues, "low" for suggestions/questions
- draft_response: Be empathetic, professional, and address the customer's concern
"""


def triage_ticket(customer_name: str, subject: str, message: str) -> AITriageResult:
    prompt = TRIAGE_PROMPT.format(
        customer_name=customer_name,
        subject=subject,
        message=message
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    # Clean markdown if present
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip()

    data = json.loads(text)

    return AITriageResult(
        category=data["category"],
        sentiment_score=data["sentiment_score"],
        urgency=data["urgency"],
        draft_response=data["draft_response"]
    )