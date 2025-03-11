from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import openai
from openai import OpenAI
from .models import Message
from dotenv import load_dotenv
import os
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import json

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

router = APIRouter()

# In-memory storage (replace with a database in production)
messages = []

# In-memory dictionary to store terms and filenames
audio_cache = {}

# Define a Pydantic model for the request body
class TranslationRequest(BaseModel):
    text: str
    target_language: str

class AudioRequest(BaseModel):
    text: str

@router.get("/")
async def root():
    """
    Root endpoint for the API.

    Returns a simple JSON message indicating that the Chrome Extension API is running.
    """
    return {"message": "Chrome Extension API is running"}

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        print(f"Received request: {request}")  # Debugging line 
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a translator. Provide direct   translations with no additional text or context."},
                {"role": "user", "content": f"Translate this word to {request.target_language}: {request.text}"}
            ],
            max_tokens=100
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

@router.post("/generate-audio")
async def generate_audio(request: AudioRequest):
    try:
        # Check if the term already exists in the cache
        if request.text in audio_cache:
            return {
                "status": "success",
                "audio_url": f"/static/audio/{audio_cache[request.text]}"
            }
        
        # Generate speech from the text
        speech_file_name = f"speech_{uuid.uuid4()}.mp3"
        speech_file_path = Path(__file__).parent / "static" / "audio" / speech_file_name
        
        # Ensure the audio directory exists
        speech_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Generate speech
        client = OpenAI()
        audio_response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=request.text
        )
        
        # Save the audio file
        audio_response.stream_to_file(str(speech_file_path))
        
        # Update the cache with the new term and filename
        audio_cache[request.text] = speech_file_name
        
        return {
            "status": "success",
            "audio_url": f"/static/audio/{speech_file_name}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
