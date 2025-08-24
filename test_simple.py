#!/usr/bin/env python3

import os
import uvicorn
from fastapi import FastAPI

app = FastAPI(title="Simple Test API")

@app.get("/")
def root():
    return {"message": "Simple test working", "port": os.environ.get("PORT", "NOT SET")}

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
