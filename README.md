# AI-Powered Educational Chatbot

This repository contains the backend for an AI-Powered Educational Chatbot. It's built using FastAPI and provides a simple REST API for interacting with the chatbot and retrieving chat history.

## ✨ Features

-   **Interactive Chat**: Engage in a conversation with an AI model.
-   **Conversation History**: All conversations are saved to a database.
-   **RESTful API**: Simple and clean API for easy integration with a frontend.
-   **Scalable**: Built with modern Python tools, ready to scale.
-   **CORS Enabled**: Allows cross-origin requests from any frontend application.

## 🛠️ Tech Stack

-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Database ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
-   **Data Validation**: [Pydantic](https://pydantic-docs.helpmanual.io/)
-   **Environment Variables**: [python-dotenv](https://pypi.org/project/python-dotenv/)
-   **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)
-   **AI Integration**: [Groq](https://groq.com/) with llama-3.3-70b-versatile model

## ✨ Features

### 🤖 AI Chatbot
- **Advanced AI Responses**: Powered by Groq's llama-3.3-70b-versatile model
- **Real-time Streaming**: Typewriter effect for natural conversation flow
- **Context Awareness**: Maintains conversation context for better responses

### 🎨 Enhanced Frontend
- **Modern UI**: Beautiful gradient design with responsive layout
- **Chat Statistics**: Real-time metrics and session tracking
- **Export Functionality**: Download chat history as JSON
- **Backend Monitoring**: Live status indicators and health checks
- **Error Handling**: Comprehensive error messages and retry mechanisms

### 🔧 Backend Features
- **RESTful API**: Clean, documented API endpoints
- **Database Integration**: Persistent chat history with PostgreSQL
- **Health Checks**: Built-in monitoring and status endpoints
- **CORS Support**: Cross-origin resource sharing enabled
- **Input Validation**: Robust data validation with Pydantic

### 🐳 Docker Support
- **Containerized Deployment**: Full Docker and Docker Compose support
- **Multi-stage Builds**: Optimized production images
- **Development Mode**: Hot reload for rapid development
- **Service Orchestration**: Automated service dependencies and health checks

## 📂 Project Structure

The project follows a clean, professional structure with organized directories:

```
ai_chatbot_project/
├── 📁 backend/                 # FastAPI backend application
├── 📁 frontend/                # Streamlit web interface
├── 📁 database/                # Database config
├── 📁 tests/                   # Test suite
├── 📄 docker-compose.yml       # Docker setup
├── 📄 requirements.txt         # Python dependencies
├── 📄 run_tests.py             # Test runner
└── 📄 README.md                # This file
```

### Directory Details

- **`backend/`** - FastAPI application with routes, services, models, and schemas
- **`frontend/`** - Streamlit web interface with enhanced UI/UX
- **`database/`** - PostgreSQL initialization scripts
- **`tests/`** - Test suite (unit, integration, docker tests)

## 🚀 Getting Started

Choose one of two deployment methods:

### 🐳 Method 1: Docker Deployment (Recommended)

**Prerequisites:** Docker and Docker Compose

1. **Clone and configure:**
   ```bash
   git clone https://github.com/your-username/ai_chatbot_project.git
   cd ai_chatbot_project
   cp .env.docker .env
   # Edit .env and add your GROQ_API_KEY
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build -d
   ```

3. **Access the application:**
   - **Frontend**: http://localhost:8501
   - **Backend API**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

### 💻 Method 2: Local Development

**Prerequisites:** Python 3.8+, PostgreSQL

1. **Setup backend:**
   ```bash
   git clone https://github.com/your-username/ai_chatbot_project.git
   cd ai_chatbot_project

   # Install dependencies
   pip install -r requirements.txt

   # Configure environment
   cp backend/.env.example .env
   # Edit .env with your GROQ_API_KEY and database settings

   # Start backend
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Setup frontend (new terminal):**
   ```bash
   cd frontend
   pip install streamlit requests pandas plotly
   streamlit run app.py
   ```

4.  **Set up environment variables:**
    Create a `.env` file in the `backend/` directory by copying the example:
    ```bash
    cp .env.example .env
    ```
    Now, edit the `.env` file with your configuration. See the Environment Variables section for details.

5.  **Run the application:**
    From within the `backend/` directory, run:
    ```bash
    uvicorn app.main:app --reload
    ```
    The application will be available at `http://127.0.0.1:8000`.

</details>

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Clean restart
docker-compose down -v && docker-compose up --build -d
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Or use the test runner
python run_tests.py
```

## ⚙️ Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `GROQ_API_KEY` | ✅ | Groq API key for AI responses |
| `POSTGRES_DB` | ✅ | Database name |
| `POSTGRES_USER` | ✅ | Database username |
| `POSTGRES_PASSWORD` | ✅ | Database password |

## 🔧 Troubleshooting

### Common Issues

**Services won't start:**
```bash
docker-compose ps
docker-compose logs -f
```

**Port conflicts:**
```bash
# Check what's using ports 8000, 8501, 5432
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac
```

**Database issues:**
```bash
docker-compose down -v && docker-compose up -d
```

**Test the endpoints:**
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:8501

## 📝 API Documentation

The API documentation is automatically generated by FastAPI and is available at:

-   **Swagger UI**: `http://127.0.0.1:8000/docs`
-   **ReDoc**: `http://127.0.0.1:8000/redoc`

### Endpoints

#### Chat

-   **`POST /chat`**: Send a message to the chatbot.
    -   **Request Body**:
        ```json
        {
          "user_message": "Hello, can you tell me about FastAPI?"
        }
        ```
    -   **Response Body**:
        ```json
        {
          "user_message": "Hello, can you tell me about FastAPI?",
          "bot_response": "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.",
          "timestamp": "2023-10-27T10:00:00.000Z"
        }
        ```

#### History

-   **`GET /history`**: Retrieve the chat history.
    -   **Query Parameters**:
        -   `limit` (int, optional, default: 10): The number of recent messages to retrieve.
    -   **Example Request**: `GET http://127.0.0.1:8000/history?limit=5`
    -   **Response Body**: A list of chat messages.

## ⚙️ Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file:

-   `DATABASE_URL`: The connection string for your database.
    -   For SQLite: `DATABASE_URL="sqlite:///./chat.db"`
    -   For PostgreSQL: `DATABASE_URL="postgresql://user:password@host:port/database_name"`
-   `AI_API_KEY`: Your API key for the AI service you are using (e.g., OpenAI's `OPENAI_API_KEY`).

## 🤝 Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.