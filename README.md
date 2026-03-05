# AI Chatbot Management System - Mini Project

## Quick Start

1. **Install Backend Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

2. **Run Backend Server:**
```bash
python app.py
```
Server runs on `http://localhost:5000`

3. **Open Frontend:**
Open `frontend/index.html` in your browser

## Features Implemented

- **Create Multiple Chatbots**: Manage multiple chatbots from one dashboard
- **Train Chatbots**: Add intent-based training data with patterns and responses
- **Real-time Chat**: Chat with trained chatbots
- **Chat History**: View conversation history for each chatbot
- **Analytics**: Track conversations and message count
- **Database**: SQLite database for persistence
- **REST API**: Complete API for chatbot operations

## API Endpoints

- `GET /api/chatbots` - List all chatbots
- `POST /api/chatbots` - Create new chatbot
- `GET /api/chatbots/<id>` - Get chatbot details
- `PUT /api/chatbots/<id>` - Update chatbot
- `DELETE /api/chatbots/<id>` - Delete chatbot
- `POST /api/chatbots/<id>/train` - Add training data
- `POST /api/chatbots/<id>/chat` - Send message to chatbot
- `GET /api/chatbots/<id>/history` - Get chat history
- `GET /api/chatbots/<id>/analytics` - Get analytics

## Project Structure

```
chatbot-system/
├── backend/
│   ├── app.py              (Flask app & routes)
│   ├── database.py         (SQLite operations)
│   ├── chatbot_engine.py   (NLP engine)
│   └── requirements.txt
└── frontend/
    └── index.html          (Dashboard UI)
```

## How to Use

1. Create a chatbot by clicking "+ New Chatbot"
2. Select the chatbot from the list
3. Train it by going to "Train Bot" tab and adding patterns/responses
4. Chat with it in the main chat area
5. View analytics in "Analytics" tab
