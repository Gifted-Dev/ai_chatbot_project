from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..crud import get_chat_history
from .. import crud, schemas
from ..services.database import get_db
from ..services.ai_engine import get_response

router = APIRouter()

@router.get("/history")
def get_history(db:Session = Depends(get_db)):
    chats = get_chat_history(db)
    return [{"user": chat.user_message, "bot": chat.bot_response} for chat in chats]
