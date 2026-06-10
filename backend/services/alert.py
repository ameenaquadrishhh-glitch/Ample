"""
Multi-channel Alert Service
Handles WhatsApp (Twilio), Gmail SMTP, and ntfy push notifications.
"""
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.config import settings
from models.schemas import IncidentCreate
import threading

def send_email_alert(incident: IncidentCreate, incident_id: str):
    try:
        msg = MIMEMultipart()
        msg["From"] = settings.email_sender
        msg["To"] = settings.email_receiver
        msg["Subject"] = f"🚨 AMPLE ALERT — {incident.threat_level} Threat Detected"

        body = f"""
AMPLE SECURITY ALERT
====================
Incident ID: {incident_id}
Threat Level: {incident.threat_level}
Video: {incident.video_filename}
Confidence: {incident.confidence_score:.2%}

{incident.detection_summary}
"""
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(settings.email_sender, settings.email_password)
            server.send_message(msg)
        print("✅ Email alert sent")
    except Exception as e:
        print(f"❌ Email alert failed: {e}")

def send_ntfy_alert(incident: IncidentCreate):
    try:
        requests.post(
            f"https://ntfy.sh/{settings.ntfy_channel}",
            data=f"🚨 {incident.threat_level} threat in {incident.video_filename} — Confidence: {incident.confidence_score:.2%}".encode("utf-8"),
            headers={"Title": "AMPLE Security Alert", "Priority": "urgent", "Tags": "warning,shield"},
        )
        print("✅ ntfy alert sent")
    except Exception as e:
        print(f"❌ ntfy alert failed: {e}")

def send_whatsapp_alert(incident: IncidentCreate):
    try:
        from twilio.rest import Client
        client = Client(settings.twilio_sid, settings.twilio_token)
        client.messages.create(
            body=f"🚨 AMPLE ALERT\nThreat: {incident.threat_level}\nVideo: {incident.video_filename}\nConfidence: {incident.confidence_score:.2%}",
            from_=settings.twilio_whatsapp,
            to=settings.whatsapp_number
        )
        print("✅ WhatsApp alert sent")
    except Exception as e:
        print(f"❌ WhatsApp alert failed: {e}")

def send_alerts(incident: IncidentCreate, incident_id: str):
    """Send all alerts in parallel threads (non-blocking)."""
    threads = [
        threading.Thread(target=send_email_alert, args=(incident, incident_id)),
        threading.Thread(target=send_ntfy_alert, args=(incident,)),
        threading.Thread(target=send_whatsapp_alert, args=(incident,)),
    ]
    for t in threads:
        t.daemon = True
        t.start()
