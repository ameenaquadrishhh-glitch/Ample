import requests
import smtplib
import threading
import time
import cv2
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# ============================================
#   AMPLE ALERT CONFIGURATION
#   Fill in your details below
# ============================================

NTFY_CHANNEL = "AMPLE-alerts-12345"  # Your phone alert channel

EMAIL_SENDER = "ameenaquadrishhh@gmail.com"        # Your Gmail
EMAIL_PASSWORD = "nyko fhxy glox vawn"          # Gmail app password
EMAIL_RECEIVER = "ameenaquadrishhh@gmail.com" # Who receives alerts

WHATSAPP_NUMBER = ""            # Number with country code
TWILIO_SID = ""
TWILIO_TOKEN = ""
TWILIO_WHATSAPP = "whatsapp:"    # Twilio sandbox number

# ============================================

os.makedirs("./incidents", exist_ok=True)

def save_screenshot(frame, camera_id):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"./incidents/incident_{camera_id}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename

def send_phone_alert(camera_id, confidence, timestamp):
    def _send():
        try:
            requests.post(
                f"https://ntfy.sh/{NTFY_CHANNEL}",
                data=f"VIOLENCE DETECTED\nCamera: {camera_id}\nConfidence: {confidence:.0%}\nTime: {timestamp}".encode("utf-8"),
                headers={
                    "Title": "!! AMPLE SECURITY ALERT !!",
                    "Priority": "urgent",
                    "Tags": "warning,rotating_light,sos"
                },
                timeout=5
            )
            print(f"[ALERT] Phone notification sent")
        except Exception as e:
            print(f"[ALERT] Phone notification failed: {e}")
    threading.Thread(target=_send).start()

def send_email_alert(camera_id, confidence, timestamp, screenshot_path=None):
    def _send():
        try:
            msg = MIMEMultipart()
            msg["Subject"] = f"!! AMPLE ALERT - Violence Detected at {camera_id} !!"
            msg["From"] = EMAIL_SENDER
            msg["To"] = EMAIL_RECEIVER

            body = f"""
AMPLE - AI Monitoring Platform for Live Emergency Detection
===========================================================

THREAT DETECTED

Camera ID   : {camera_id}
Confidence  : {confidence:.0%}
Time        : {timestamp}
Status      : IMMEDIATE RESPONSE REQUIRED

This is an automated alert from AMPLE.
Please review the incident and take appropriate action.

- AMPLE Security System
            """
            msg.attach(MIMEText(body, "plain"))

            if screenshot_path and os.path.exists(screenshot_path):
                with open(screenshot_path, "rb") as f:
                    img = MIMEImage(f.read())
                    img.add_header("Content-Disposition", "attachment", filename="incident.jpg")
                    msg.attach(img)

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                server.send_message(msg)
            print(f"[ALERT] Email sent to {EMAIL_RECEIVER}")
        except Exception as e:
            print(f"[ALERT] Email failed: {e}")
    threading.Thread(target=_send).start()

def send_whatsapp_alert(camera_id, confidence, timestamp):
    def _send():
        try:
            from twilio.rest import Client
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            client.messages.create(
                from_=TWILIO_WHATSAPP,
                to=f"whatsapp:{WHATSAPP_NUMBER}",
                body=f"AMPLE ALERT\nViolence detected at {camera_id}\nConfidence: {confidence:.0%}\nTime: {timestamp}"
            )
            print(f"[ALERT] WhatsApp sent to {WHATSAPP_NUMBER}")
        except Exception as e:
            print(f"[ALERT] WhatsApp failed: {e}")
    threading.Thread(target=_send).start()

def fire_all_alerts(frame, camera_id, confidence):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    screenshot = save_screenshot(frame, camera_id)
    print(f"\n{'='*50}")
    print(f"  !! AMPLE ALERT FIRED !!")
    print(f"  Camera   : {camera_id}")
    print(f"  Confidence: {confidence:.0%}")
    print(f"  Time     : {timestamp}")
    print(f"  Screenshot: {screenshot}")
    print(f"{'='*50}\n")
    send_phone_alert(camera_id, confidence, timestamp)
    send_email_alert(camera_id, confidence, timestamp, screenshot)

if __name__ == "__main__":
    print("Testing AMPLE alert system...")
    send_phone_alert("CAM-01", 0.94, time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Phone alert sent. Check your ntfy app.")