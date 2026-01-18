# Fitness AI Agent 💪

An AI-powered fitness tracking and goal management system built with **LangGraph**, **FastAPI**, and **Streamlit**.

## Features

- 🤖 **Conversational AI Interface** - Chat naturally about your meals and fitness goals
- 🔄 **Multi-LLM Support** - Switch between Gemini, OpenAI, Groq, or Ollama (local)
- 🍎 **Smart Food Logging** - Automatically parse and estimate calories from natural language
- 🎯 **Goal Management** - Set and track weight loss, muscle gain, or maintenance goals
- 📊 **Progress Summaries** - Get daily, weekly, and monthly fitness insights
- 🔔 **Smart Reminders** - Optional Google Calendar integration for meal logging reminders
- 📱 **Activity Tracking** - Optional Google Fit integration for exercise data

## Architecture

### Backend (`/backend`)
- **FastAPI** - RESTful API server
- **LangGraph** - Agentic workflow orchestration
- **Multi-LLM Support** - Gemini, OpenAI, Groq, or Ollama (local)
- **Supabase** - PostgreSQL database
- **Google APIs** - Calendar and Fit integration (optional)

### Frontend (`/frontend`)
- **Streamlit** - Interactive web UI
- Chat interface for conversational interaction
- Goal setting forms
- Weekly summary dashboards

## Project Structure

```
fitness-ai-agent/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration
│   │   ├── dependencies.py      # Dependency injection
│   │   ├── graph/               # LangGraph workflow
│   │   ├── nodes/               # Graph nodes
│   │   ├── tools/               # LLM, DB, API clients
│   │   ├── services/            # Business logic
│   │   ├── api/                 # API endpoints
│   │   ├── models/              # Data models
│   │   └── utils/               # Utilities
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── streamlit_app.py         # Main Streamlit app
│   ├── components/              # UI components
│   └── services/                # API client
├── scripts/                     # Utility scripts
├── tests/                       # Unit tests
└── README.md
```

## Setup

### Prerequisites
- Python 3.11+
- Supabase account
- **LLM Provider** (choose one):
  - Gemini API key (free, recommended for beginners)
  - OpenAI API key (paid, best quality)
  - Groq API key (free, fastest)
  - Ollama installed locally (free, private, offline)
- Google Cloud credentials (optional, for Calendar/Fit)

### 1. Clone and Install

```bash
cd fitness-ai-agent

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
pip install streamlit httpx
```

### 2. Configure Environment

Copy `.env` and fill in your credentials:

```bash
cp .env .env.local
# Edit .env with your API keys
```

Required variables:
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase API key
- `LLM_PROVIDER` - Choose: `gemini`, `openai`, `groq`, or `ollama`
- API key for your chosen provider (see [LLM_PROVIDER_GUIDE.md](LLM_PROVIDER_GUIDE.md))
- `SECRET_KEY` - Random secret for JWT tokens

**📖 See [LLM_PROVIDER_GUIDE.md](LLM_PROVIDER_GUIDE.md) for detailed setup instructions for each provider.**

### 3. Set Up Database

Run the migration script to get SQL commands:

```bash
python scripts/migrate_db.py
```

Copy the SQL commands and run them in your Supabase SQL editor.

### 4. Run the Application

**Start the backend:**
```bash
cd backend
uvicorn app.main:app --reload
```

**Start the frontend:**
```bash
cd frontend
streamlit run streamlit_app.py
```

The app will be available at:
- Backend API: http://localhost:8000
- Frontend UI: http://localhost:8501
- API Docs: http://localhost:8000/docs

## Usage

### Chat Interface

Simply chat with the AI agent:

- **Log food**: "I ate 2 eggs and toast for breakfast"
- **Set goals**: "I want to lose weight, target 1800 calories per day"
- **Get summary**: "Show me my weekly summary"
- **Ask questions**: "How many calories should I eat to lose weight?"

### API Endpoints

- `POST /api/chat` - Send chat messages
- `POST /api/goals/{user_id}` - Set/update goals
- `GET /api/goals/{user_id}` - Get current goal
- `GET /api/summary/{user_id}?period=weekly` - Get summary

## Development

### Running Tests

```bash
cd tests
pytest
```

### Docker Deployment

```bash
cd backend
docker build -t fitness-ai-agent .
docker run -p 8000:8000 --env-file .env fitness-ai-agent
```

## LangGraph Workflow

The agent uses a graph-based workflow:

1. **Route Intent** - Classify user message (food logging, goal setting, summary, etc.)
2. **Execute Node** - Route to appropriate handler:
   - `parse_food` → `estimate_calories` - For food logging
   - `goal_manager` - For goal setting
   - `summary_weekly` - For summaries
   - `clarification` - When intent is unclear
3. **Return Response** - Generate user-friendly response

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues or questions, please open a GitHub issue.

---

Built with ❤️ using LangGraph, FastAPI, and Streamlit
