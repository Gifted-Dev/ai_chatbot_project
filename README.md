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
-   **AI Integration**: (e.g., OpenAI, Hugging Face, etc. - *Please specify the service you are using*)

## 📂 Project Structure

The project follows a standard FastAPI application structure:

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── crud.py           # Database Create, Read, Update, Delete operations
│   │   ├── main.py           # FastAPI application entry point
│   │   ├── models.py         # SQLAlchemy database models
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── chatbot.py    # API routes for chat functionality
│   │   │   └── history.py    # API routes for chat history
│   │   ├── schemas.py        # Pydantic data validation schemas
│   │   └── services/
│   │       ├── __init__.py
│   │       └── database.py   # Database session and engine setup
│   ├── .env.example          # Example environment variables
│   └── requirements.txt      # Python dependencies
└── README.md
```

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

-   Python 3.8+
-   A package manager like `pip`

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd ai_chatbot_project/backend
    ```

2.  **Create and activate a virtual environment:**
    -   On macOS and Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file is assumed. If you don't have one, you can create it with `pip freeze > requirements.txt` after installing the necessary packages like `fastapi`, `uvicorn`, `sqlalchemy`, `pydantic`, `python-dotenv`, and your database driver e.g. `psycopg2-binary` or `pysqlite3`)*

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