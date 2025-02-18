from sqlalchemy import Column, Integer, String, DateTime
# from sqlalchemy.orm import relationship
from sqlalchemy import func
from .services.database import Base

# from datetime import datetime, timezone


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    bot_response = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())