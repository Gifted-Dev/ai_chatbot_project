import streamlit as st
import requests
import time
import os
from datetime import datetime
import json

# Page configuration with enhanced styling
st.set_page_config(
    page_title="AI-Powered Educational Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }

    /* Header styling */
    .header-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }

    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }

    /* Chat container styling */
    .chat-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* Status indicators */
    .status-indicator {
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem 0;
    }

    .status-online {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }

    .status-offline {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }

    /* Sidebar styling */
    .sidebar-content {
        background-color: #f1f3f4;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }

    /* Message styling */
    .user-message {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }

    .bot-message {
        background-color: #f3e5f5;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }

    /* Loading animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Get backend URL from environment variable (for Docker compatibility)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "backend_status" not in st.session_state:
    st.session_state.backend_status = "unknown"
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

# Header section
st.markdown("""
<div class="header-container">
    <div class="header-title">🤖 AI Educational Chatbot</div>
    <div class="header-subtitle">Your intelligent learning companion powered by advanced AI</div>
</div>
""", unsafe_allow_html=True)

# Sidebar with enhanced features
with st.sidebar:
    st.markdown("### 📊 Chat Statistics")

    # Backend status check
    def check_backend_status():
        try:
            response = requests.get(f"{BACKEND_URL}/docs", timeout=5)
            return "online" if response.status_code == 200 else "offline"
        except:
            return "offline"

    # Check backend status
    if st.button("🔄 Check Backend Status"):
        st.session_state.backend_status = check_backend_status()

    # Display status
    status_class = "status-online" if st.session_state.backend_status == "online" else "status-offline"
    status_text = "🟢 Online" if st.session_state.backend_status == "online" else "🔴 Offline"

    st.markdown(f"""
    <div class="status-indicator {status_class}">
        Backend Status: {status_text}
    </div>
    """, unsafe_allow_html=True)

    # Chat statistics
    st.metric("Total Messages", st.session_state.total_messages)
    st.metric("Current Session", len(st.session_state.messages))

    # Chat history management
    st.markdown("### 🗂️ Chat Management")

    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

    if st.button("💾 Export Chat"):
        if st.session_state.messages:
            chat_export = {
                "timestamp": datetime.now().isoformat(),
                "messages": st.session_state.messages,
                "total_messages": len(st.session_state.messages)
            }
            st.download_button(
                label="📥 Download Chat JSON",
                data=json.dumps(chat_export, indent=2),
                file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

    # Help section
    st.markdown("### ❓ Help & Tips")
    with st.expander("How to use"):
        st.markdown("""
        - Type your question in the chat input below
        - Press Enter or click Send to submit
        - The AI will respond with helpful information
        - Use the sidebar to manage your chat session
        """)

    with st.expander("Features"):
        st.markdown("""
        - 🤖 AI-powered responses
        - 💬 Real-time chat interface
        - 📊 Chat statistics
        - 💾 Export chat history
        - 🔄 Backend status monitoring
        """)

# Main chat interface
st.markdown("### 💬 Chat Interface")

# Display chat messages with enhanced styling
for i, message in enumerate(st.session_state.messages):
    if message["role"] == "user":
        st.markdown(f"""
        <div class="user-message">
            <strong>👤 You:</strong><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bot-message">
            <strong>🤖 AI Assistant:</strong><br>
            {message["content"]}
        </div>
        """, unsafe_allow_html=True)

# Enhanced response streaming function
def stream_response(text: str):
    """Stream response with realistic typing effect"""
    words = text.split()
    for i, word in enumerate(words):
        yield " ".join(words[:i+1])
        time.sleep(0.03)  # Faster streaming for better UX

# Chat input with enhanced error handling
prompt = st.chat_input("💭 What would you like to learn about today?")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_messages += 1

    # Display user message immediately
    st.markdown(f"""
    <div class="user-message">
        <strong>👤 You:</strong><br>
        {prompt}
    </div>
    """, unsafe_allow_html=True)

    # Show loading indicator
    with st.spinner("🤔 AI is thinking..."):
        try:
            # Make API request
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"user_message": prompt},
                timeout=30
            )

            if response.status_code == 200:
                bot_reply = response.json().get("bot_response", "I apologize, but I couldn't generate a response.")

                # Create placeholder for streaming response
                response_placeholder = st.empty()

                # Stream the response
                full_response = ""
                for partial_response in stream_response(bot_reply):
                    full_response = partial_response
                    response_placeholder.markdown(f"""
                    <div class="bot-message">
                        <strong>🤖 AI Assistant:</strong><br>
                        {partial_response}
                    </div>
                    """, unsafe_allow_html=True)

                # Add to session state
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                st.session_state.total_messages += 1

            else:
                error_msg = f"❌ Error: Backend returned status code {response.status_code}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except requests.exceptions.Timeout:
            error_msg = "⏰ Request timed out. Please try again."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except requests.exceptions.ConnectionError:
            error_msg = "🔌 Cannot connect to backend. Please check if the backend service is running."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

        except Exception as e:
            error_msg = f"❌ Unexpected error: {str(e)}"
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>
        🤖 Powered by AI | Built with Streamlit & FastAPI |
        <a href="{}/docs" target="_blank">API Documentation</a>
    </small>
</div>
""".format(BACKEND_URL), unsafe_allow_html=True)
    