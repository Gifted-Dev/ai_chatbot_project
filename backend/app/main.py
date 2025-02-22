from fastapi import FastAPI
from sqlalchemy.orm import Session
from .services.database import Base, engine
from .routes import chatbot
from . import models, crud, schemas
from fastapi.middleware.cors import CORSMiddleware

# This will create the tables defined in your models
Base.metadata.create_all(bind=engine)


app = FastAPI(title="AI-Powered Educational Chatbot")


# Enable CORS for  all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chatbot.router)


        
