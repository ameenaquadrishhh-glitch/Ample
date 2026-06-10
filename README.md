# 🛡️ AMPLE — Agentic Monitoring and Proactive Law Enforcement Engine

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-green)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-purple)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-teal)

> AI-powered security operations platform for real-time violence detection, threat assessment, and automated incident reporting.

---

## 🚀 Features

- 🎥 **Video Analysis** — Upload CCTV footage for automated processing
- 🔍 **Violence Detection** — YOLOv8-powered real-time detection
- ⚠️ **Threat Level Scoring** — LOW / MEDIUM / HIGH / CRITICAL classification
- 📋 **AI Incident Reports** — Auto-generated reports via Claude AI
- 📊 **Command Center Dashboard** — Live stats and incident history
- 🔔 **Multi-channel Alerts** — WhatsApp (Twilio), Gmail SMTP, ntfy push

---

## 🏗️ Architecture

```
Frontend (Next.js 14)  →  Backend (FastAPI)  →  AI Engine (YOLOv8)
         ↕                       ↕                      ↕
    Vercel CDN           Render (Docker)         Claude API (Reports)
         ↕                       ↕
    Supabase DB          Supabase Storage
```

---

## 📁 Project Structure

```
ample/
├── frontend/          # Next.js 14 dashboard
│   ├── app/           # App router pages
│   ├── components/    # Reusable UI components
│   └── lib/           # API clients & utilities
├── backend/           # FastAPI server
│   ├── routers/       # API route handlers
│   ├── services/      # Business logic (detection, reports, alerts)
│   ├── models/        # Pydantic schemas
│   └── core/          # Config & database connection
└── docs/              # Architecture diagrams & notes
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, Tailwind CSS, shadcn/ui |
| Backend | FastAPI, Python 3.10+ |
| AI Detection | YOLOv8 (Ultralytics) |
| Report Generation | Claude API (Anthropic) |
| Database | Supabase (PostgreSQL) |
| File Storage | Supabase Storage |
| Deployment | Vercel (frontend), Render (backend) |
| Alerts | Twilio WhatsApp, Gmail SMTP, ntfy |

---

## 📦 Setup

See [docs/setup.md](docs/setup.md) for full installation guide.

---

## 🗺️ Roadmap

- [x] Phase 0 — Violence detection engine (Python scripts)
- [ ] Phase 1 — Full platform MVP (Dashboard + API + DB)
- [ ] Phase 2 — Multi-camera + weapon detection + alerts
- [ ] Phase 3 — Agentic workflow architecture
- [ ] Phase 4 — Enterprise-grade platform

---

## 👩‍💻 Author

**Ameena Quadri** — CS Student | AI/ML Engineer
- GitHub: [@ameenaquadrishhh-glitch](https://github.com/ameenaquadrishhh-glitch)

---

*Built for NVIDIA Agentic AI Hackathon & Prettiflow Cohort 1*
