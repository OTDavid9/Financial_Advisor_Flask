import os
from fastapi import FastAPI, HTTPException, Request, WebSocket
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
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

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index copy.html", {"request": request})

class WebSocketHandler:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket

    async def send_response(self, response: dict):
        await self.websocket.send_json(response)

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    handler = WebSocketHandler(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            query_request = QueryRequest(query=data)
            if not query_request.query.strip():
                await handler.send_response({"error": "User query cannot be empty"})
                continue
            
            messages = [{'role': 'user', 'parts': [persona]}]
            response = model.generate_content(messages)
            messages.append({'role': 'model', 'parts': [response.text]})
            messages.append({'role': 'user', 'parts': [query_request.query]})
            response = model.generate_content(messages)
            await handler.send_response({"response": str(response.text)})
    
    except Exception as e:
        await handler.send_response({"error": "An unexpected error occurred"})
        await websocket.close()

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)
