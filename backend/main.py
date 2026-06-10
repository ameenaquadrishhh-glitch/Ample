from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import video, incidents
import uvicorn

app = FastAPI(
    title="AMPLE API",
    description="Agentic Monitoring and Proactive Law Enforcement Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(video.router, prefix="/api/v1/video", tags=["Video Processing"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["Incidents"])

@app.get("/")
def root():
    return {"status": "online", "platform": "AMPLE", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
