# Personal Assistant Agent 🤖

A Python-based AI agent that connects to your Gmail and Google Calendar. Ask it anything in plain English — it figures out which tool to use and gets it done. Runs 100% free and offline using Ollama locally, switches to Anthropic Claude in production with one environment variable.

---

## What it does

- 📧 **Read emails** — fetch and summarize your latest inbox
- 📝 **Draft emails** — agent creates drafts, never sends directly (safety first)
- 📅 **Read calendar** — see upcoming events and meetings
- 🗓️ **Create events** — add new events to your Google Calendar
- 🤖 **Agent brain** — LangGraph + LLM decides which tool to use automatically
- 🦙 **Free local dev** — runs on Ollama llama3.2, zero cost, no internet needed
- ☁️ **Production ready** — one env var switches to Anthropic Claude

---

## How agents work vs RAG

```
RAG:    Question → Search docs → Answer

Agent:  Question → Think → Pick tool → Use it → Think again → Answer
                    ↑___________________________________|
                         (loops until task is done)
```

The agent reasons in a loop, picking the right tool automatically based on what you ask.

---

## Example conversations

```
You:   "What are my latest emails?"
Agent: Calls tool_read_emails → summarizes your inbox

You:   "Draft an email to john@email.com about the project update"
Agent: Calls tool_create_draft → creates draft in Gmail for you to review

You:   "What meetings do I have this week?"
Agent: Calls tool_get_events → lists your calendar events

You:   "Schedule a meeting called standup tomorrow at 10am to 11am"
Agent: Calls tool_create_event → adds event to Google Calendar
```

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Language | Python 3.12 | Industry standard for AI |
| LLM (dev) | Ollama `llama3.2` | Free, offline, no API key |
| LLM (prod) | Anthropic `claude-sonnet-4-6` | One env var switch |
| Agent framework | LangGraph | Agent orchestration |
| Backend | FastAPI | Python equivalent of Express.js |
| Email | Gmail API | Read inbox, create drafts |
| Calendar | Google Calendar API | Read and create events |
| Auth | Google OAuth 2.0 | Secure Gmail/Calendar access |

---

## Project Structure

```
personal-agent/
├── agent.py              # LangGraph agent brain + tool definitions
├── main.py               # FastAPI server
├── gmail_tool.py         # Gmail read + draft creation
├── calendar_tool.py      # Google Calendar read + create events
├── test_agent.py         # Test all agent capabilities
├── test_gmail.py         # Test Gmail connection only
├── test_calendar.py      # Test Calendar connection only
├── credentials.json      # Google OAuth credentials (never commit!)
├── token.json            # Auto-generated auth token (never commit!)
├── .env                  # API keys (never commit!)
├── .gitignore
└── requirements.txt
```

---

## Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed locally
- Google Cloud project with Gmail + Calendar APIs enabled

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/TpPrachi/personal_assistant_agent.git
cd personal_assistant_agent
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn anthropic python-dotenv \
  google-auth-oauthlib google-auth-httplib2 google-api-python-client \
  langgraph langchain-anthropic langchain-core langchain-ollama
```

### 4. Set up environment variables
Create `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-...   # only needed for production
```

### 5. Pull Ollama model
```bash
ollama pull llama3.2
ollama serve
```

### 6. Set up Google OAuth

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project called `personal-agent`
3. Enable **Gmail API** and **Google Calendar API**
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth Client ID**
5. Application type: **Desktop App**
6. Download JSON → save as `credentials.json` in project root
7. Go to **OAuth Consent Screen → Audience → Test Users**
8. Add your Gmail address as a test user

### 7. Authenticate with Google
```bash
python3 test_gmail.py
```
Browser opens → log in → allow permissions → `token.json` saved automatically.

---

## Running the app

### Test the agent
```bash
# Make sure Ollama is running
ollama serve

# Activate venv
source venv/bin/activate

# Run tests
python3 test_agent.py
```

### Start the API server
```bash
uvicorn main:app --reload
```

### Ask the agent via API
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are my latest emails?"}'
```

---

## Dev vs Production

| | Development | Production |
|---|---|---|
| `APP_ENV` | unset (default) | `production` |
| LLM | Ollama llama3.2 | Anthropic Claude |
| Cost | Free | Pay per token |
| Internet | Not needed | Required |

```bash
# Development (default — uses Ollama)
python3 test_agent.py

# Production (uses Claude)
APP_ENV=production ANTHROPIC_API_KEY=sk-ant-... python3 test_agent.py
```

---

## Gmail Safety — Drafts Only

The agent **never sends emails directly**. It always creates drafts that you review in Gmail before sending. This is intentional — you stay in control.

To send: open Gmail → Drafts → review → send manually.

---

## Google OAuth Scopes

| Scope | Why |
|---|---|
| `gmail.readonly` | Read inbox and emails |
| `gmail.compose` | Create drafts |
| `calendar.readonly` | Read events |
| `calendar.events` | Create events |

---

## How the Agent Thinks

```
You ask a question
        │
        ▼
LangGraph agent receives it
        │
        ▼
LLM reads the question + available tools
        │
        ▼
LLM decides which tool to call
        │
        ▼
Tool executes (Gmail / Calendar API)
        │
        ▼
LLM reads the tool result
        │
        ▼
LLM decides if done or needs another tool
        │
        ▼
Final answer returned to you
```

---

## Important — Never commit secrets!

Your `.gitignore` must contain:
```
token.json
credentials.json
.env
venv/
__pycache__/
*.pyc
```

GitHub's secret scanning will block your push if these files are committed.

---

## Roadmap

- [x] FastAPI backend
- [x] Gmail read emails
- [x] Gmail create drafts (safety first)
- [x] Google Calendar read events
- [x] Google Calendar create events
- [x] LangGraph agent with automatic tool selection
- [x] Ollama local dev → Claude production switch
- [ ] React chat UI
- [ ] Streaming responses (see agent think step by step)
- [ ] Web search tool
- [ ] Deploy to production

---

## Related Project

Built as a follow-up to the [RAG Demo](https://github.com/TpPrachi/rag-demo) — a Node.js RAG system with ChromaDB, Ollama, streaming responses and a React chat UI.

## Python vs JavaScript Cheat Sheet

| JavaScript | Python |
|---|---|
| `const x = 5` | `x = 5` |
| `console.log()` | `print()` |
| `async/await` | `async/await` |
| `package.json` | `requirements.txt` |
| `npm install` | `pip install` |
| `node index.js` | `python main.py` |
| `{}` object | `{}` dict |
| `array.map()` | `[x for x in array]` |

## License

MIT