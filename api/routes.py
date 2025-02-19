from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import openai
from openai import OpenAI
from .models import Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

# In-memory storage (replace with a database in production)
messages = []

# Define a Pydantic model for the request body
class TranslationRequest(BaseModel):
    text: str
    target_language: str

@router.get("/")
async def root():
    return {"message": "Chrome Extension API is running"}

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        print(f"Received request: {request}")  # Debugging line 
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a translator. Provide only single word translations with no additional text or context."},
                {"role": "user", "content": f"Translate this word to {request.target_language}: {request.text}"}
            ],
            max_tokens=20
        )
        translated_text = response.choices[0].message.content.strip()
        return {"translated_text": translated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/messages")
async def create_message(message: Message):
    messages.append(message)
    return {"status": "success", "message": message}

@router.get("/messages")
async def get_messages():
    return messages

# New test endpoint
@router.post("/test")
async def test_endpoint(data: dict):
    print("Test data received:", data)
    return {"status": "success", "received_data": data}

# Function to translate a sample text to Spanish
