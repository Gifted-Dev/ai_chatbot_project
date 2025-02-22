from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChatRequest(BaseModel):
    user_message: str
    
class ChatResponse(BaseModel):
    user_message: str
    bot_response: Optional[str]
    timestamp: datetime
    
    class Config:
       from_attributes : True
    


 
        
