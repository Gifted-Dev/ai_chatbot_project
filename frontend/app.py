import streamlit as st 
import requests
import time

st.set_page_config(page_title="AI-Powered Educational Chatbot", page_icon="🏫")
st.title("AI Educational Chatbot")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Display chat message from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Function to give bot like reply
def response_bot(bot: str):
    lines = bot.split("\n")  # Preserve markdown formatting
    for line in lines:
        yield line + "\n\n"  # Add extra spacing for readability
        time.sleep(0.05)

prompt = st.chat_input("What would you like to know?")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        # Add user to chat history     
        st.markdown(f"You: {prompt}")
        
    response = requests.post(f"http://127.0.0.1:8000/chat", json={"user_message" : prompt})
    
    if response.status_code == 200:
        bot_reply = response.json().get("bot_response", "No response")
        
        with st.chat_message("assistant"):
            response_container = st.empty()  # Placeholder for streaming text

            full_reply = ""  # To store full response for history
            for word in response_bot(bot_reply):
                full_reply += word
                response_container.markdown(full_reply) 
            
        st.session_state.messages.append({"role": "assistant", "content": full_reply})
# st.chat_message
    