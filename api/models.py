from pydantic import BaseModel
from typing import Optional

# Example data model
class Message(BaseModel):
    content: str
    user_id: Optional[str] = None 


