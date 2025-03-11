from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
desc="This is the backend for the Darshini project, a language learning assistant focused on South Indian languages. It provides APIs for text translation, audio generation, and interactive learning workflows."
app = FastAPI(
    description=desc
)

# Configure CORS to allow requests from your Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://*"],  # Allow all Chrome extensions
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 