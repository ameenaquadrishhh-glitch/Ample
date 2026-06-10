"""
AI Incident Report Generator using Claude API
"""
import anthropic
from models.schemas import DetectionResult
from core.config import settings

def generate_report(detection: DetectionResult, filename: str) -> str:
    try:
        client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

        prompt = f"""You are an AI security analyst for the AMPLE platform.
Generate a professional incident report based on the following detection data.

VIDEO FILE: {filename}
VIOLENCE DETECTED: {detection.violence_detected}
CONFIDENCE SCORE: {detection.confidence_score:.2%}
THREAT LEVEL: {detection.threat_level}
FRAMES ANALYZED: {detection.frame_count}
DETECTION SUMMARY: {detection.detection_summary}

Write a concise, professional incident report with these sections:
1. INCIDENT SUMMARY
2. THREAT ASSESSMENT
3. DETECTION DETAILS
4. RECOMMENDED ACTIONS

Keep it factual and under 300 words."""

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except Exception as e:
        return f"Report generation failed: {str(e)}. Manual review required."
