from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Agentic AI is running!"}

@app.get("/run")
def run():
    result = subprocess.run(
        ["python", "inference.py", "--task", "easy", "--episodes", "2"],
        capture_output=True,
        text=True
    )
    return {
        "output": result.stdout,
        "error": result.stderr
    }
