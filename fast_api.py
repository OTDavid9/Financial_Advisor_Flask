import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
from system_messages import persona
import uvicorn

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-pro')

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/ask")
async def ask_question(request: Request, query_request: QueryRequest):
    try:
        query = query_request.query
        
        if not query.strip():
            raise HTTPException(status_code=400, detail="User query cannot be empty")
        
        messages = [{'role': 'user', 'parts': [persona]}]
        response = model.generate_content(messages)
        messages.append({'role': 'model', 'parts': [response.text]})
        messages.append({'role': 'user', 'parts': [query]})
        response = model.generate_content(messages)
        
        return JSONResponse(content={"response": str(response.text)})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)

