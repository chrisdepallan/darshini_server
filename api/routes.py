from fastapi import APIRouter
from .models import Message

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
        # Call OpenAI API for translation (this is a placeholder, replace with actual API call)
        response = openai.Completion.create(
            engine="text-davinci-003",
           prompt=f"Translate the following text to {request.target_language}: {request.text}",
            max_tokens=100
        )
        translated_text = response.choices[0].text.strip()
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