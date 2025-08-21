from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import uvicorn

# App metadata
port = 8080
name = "myapp"
version = "v0.1.4"

app = FastAPI()

# Response models
class MessageResponse(BaseModel):
    message: str

class AboutResponse(BaseModel):
    service: str
    version: str

class HealthResponse(BaseModel):
    status: str

# Fibonacci function (same as Go version, recursive)
def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

@app.get("/api/cpu", response_model=MessageResponse)
def cpu(index: int = Query(..., description="Fibonacci index")):
    try:
        n = fib(index)
    except RecursionError:
        raise HTTPException(status_code=400, detail="Index too large, recursion limit exceeded")
    msg = f"Testing CPU load: Fibonacci index is {index}, number is {n}"
    return {"message": msg}

@app.get("/about", response_model=AboutResponse)
def about():
    return {"service": name, "version": version}

@app.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port)
