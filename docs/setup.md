# AMPLE — Local Development Setup

## Prerequisites
- Python 3.10+
- Node.js 18+
- A Supabase account (free tier is fine)
- An Anthropic API key

## 1. Clone the repo
git clone https://github.com/ameenaquadrishhh-glitch/Ample.git
cd Ample

## 2. Backend setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Fill in your .env values, then:
uvicorn main:app --reload
# Runs at http://localhost:8000
# API docs at http://localhost:8000/docs

## 3. Frontend setup
cd frontend
npm install
cp .env.example .env.local
# Set NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
npm run dev
# Runs at http://localhost:3000

## 4. Supabase SQL — run this in your Supabase SQL editor
create table incidents (
  id uuid default gen_random_uuid() primary key,
  created_at timestamptz default now(),
  video_filename text not null,
  threat_level text not null,
  confidence_score float not null,
  violence_detected boolean not null,
  frame_count int not null,
  detection_summary text,
  ai_report text,
  video_url text,
  thumbnail_url text
);

## 5. Deployment
- Frontend: Import repo on vercel.com, set NEXT_PUBLIC_BACKEND_URL env var
- Backend: Create Web Service on render.com, point to /backend folder
