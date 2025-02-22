import os
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# Add API key
client = Groq(api_key = os.getenv("GROQ_API_KEY"))

def get_response(user_message: str) -> str:
    
    system_prompt = (
            "You are an AI educational assistant. Your goal is to provide helpful, "
            "accurate, and engaging educational content. Explain concepts clearly "
            "and provide examples when appropriate."
            "if not explicity specified, give a concise and simple to understand explanation"
            "You can then ask if the user understands or want a indepth explanation"
            )
    
    response = client.chat.completions.create(
        messages=[
            # setting optional system message
            {
            "role": "system",
            "content": system_prompt
            },
            # message for the bot to reply to
            {
                "role": "user",
                "content": user_message
            }
        ],
        
        
        # setting up the language model to use
        model="llama-3.3-70b-versatile"
    )
    
    return response.choices[0].message.content