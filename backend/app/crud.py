from sqlalchemy.orm import Session
from . import models, schemas


# CREATE - Send a new chat message
def save_chat(db: Session, chat: schemas.ChatRequest, response: str):
    chat_entry  = models.ChatMessage(user_id=chat.user_id, user_message=chat.user_message, bot_response=response)
    db.add(chat_entry)
    db.commit()
    db.refresh(chat_entry)
    return chat_entry

# READ - Get chat history for a specific user
def get_chat_history(db: Session, user_id: int, limit: int = 10):
    return db.query(models.ChatMessage)\
            .filter(models.ChatMessage.user_id == user_id)\
            .orderby(models.ChatMessage.timestamp.desc())\
            .limit(limit)\
            .all()
            