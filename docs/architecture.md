# AMPLE Architecture

## Data Flow

```
User uploads video
       ↓
FastAPI /api/v1/video/upload
       ↓
Supabase Storage (raw video saved)
       ↓
YOLOv8 Detection Service
  - Frame extraction
  - Violence/weapon detection
  - Confidence scoring
  - Threat level assignment
       ↓
Claude AI Report Service
  - Generates structured incident report
       ↓
Supabase DB (incident record saved)
       ↓
Alert Service (if HIGH or CRITICAL)
  - WhatsApp via Twilio
  - Gmail SMTP
  - ntfy push
       ↓
Frontend Dashboard updates
```

## Threat Level Logic

| Confidence Score | Threat Level |
|-----------------|-------------|
| 0 - 0.3         | LOW         |
| 0.3 - 0.6       | MEDIUM      |
| 0.6 - 0.85      | HIGH        |
| 0.85+           | CRITICAL    |
