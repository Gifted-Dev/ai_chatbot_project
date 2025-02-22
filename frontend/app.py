import streamlit as st 
import requests

st.set_page_config(page_title="AI-Powered Educational Chatbot", page_icon="🏫")
st.title("AI Educational Chatbot")

prompt = st.chat_input("What would you like to know")

if prompt:
    