# Supabase Setup

## Tables

### incidents
```sql
create table incidents (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  video_filename text not null,
  threat_level text check (threat_level in ('LOW','MEDIUM','HIGH','CRITICAL')),
  confidence_score float,
  violence_detected boolean default false,
  frame_count int,
  detection_summary text,
  ai_report text,
  video_url text,
  thumbnail_url text
);
```

### alerts
```sql
create table alerts (
  id uuid primary key default gen_random_uuid(),
  incident_id uuid references incidents(id),
  created_at timestamptz default now(),
  channel text check (channel in ('whatsapp','email','ntfy')),
  status text check (status in ('sent','failed','pending')),
  message text
);
```
