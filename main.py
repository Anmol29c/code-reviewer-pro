from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Code Reviewer AI API"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/review")
async def review_code(data: dict):
    code = data.get("code", "")
    
    if not code or len(code) < 5:
        return {"error": "Code too short"}
    
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"Review this code for security, performance, quality, and bugs:\n\n{code}"
        response = model.generate_content(prompt)
        
        return {
            "review": response.text,
            "status": "success"
        }
    except Exception as e:
        return {"error": str(e), "status": "failed"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)