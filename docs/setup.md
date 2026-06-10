# AMPLE — Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- Git

## 1. Clone the repo

```bash
git clone https://github.com/ameenaquadrishhh-glitch/Ample.git
cd Ample
```

## 2. Backend setup

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp ../.env.example .env
# Fill in your .env values
uvicorn main:app --reload
```

## 3. Frontend setup

```bash
cd frontend
npm install
cp ../.env.example .env.local
# Fill in your .env.local values
npm run dev
```

## 4. Supabase setup

See [docs/supabase.md](supabase.md)
