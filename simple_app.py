from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uvicorn
import os

print("🚀 Starting Google Maps Scraper API...")
print(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")

app = FastAPI(title="Google Maps Scraper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Google Maps Scraper API", 
        "version": "1.0.0", 
        "status": "active",
        "port": os.environ.get('PORT', 'NOT SET')
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "timestamp": datetime.now().isoformat(),
        "port": os.environ.get('PORT', 'NOT SET')
    }

if __name__ == "__main__":
    # Get port from environment, default to 8000 if not set
    port = int(os.environ.get("PORT", 8000))
    print(f"🌐 Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
