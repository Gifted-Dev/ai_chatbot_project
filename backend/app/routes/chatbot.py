from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..services.database import get_db
from ..services.ai_engine import get_response
from ..schemas import ChatResponse

router = APIRouter()

@router.post("/chat")
def create_chat(chat: schemas.ChatRequest, db: Session = Depends(get_db)):
    # call AI engine to get response
    response = get_response(chat.user_message)
    chat_entry = crud.save_chat(db, chat, response)
    return ChatResponse.model_validate(chat_entry, from_attributes=True)
    