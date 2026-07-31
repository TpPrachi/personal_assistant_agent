# Personal Assistant Agent 🤖

A Python-based AI agent that connects to your Gmail and Google Calendar. Ask it anything in plain English — it figures out which tool to use and gets it done. Runs 100% free and offline using Ollama locally, switches to Anthropic Claude in production with one environment variable.

---

## What it does

- 📧 **Read emails** — fetch and summarize your latest inbox
- 📝 **Draft emails** — agent creates drafts, never sends directly (safety first)
- 📅 **Read calendar** — see upcoming events and meetings
- 🗓️ **Create events** — add new events to your Google Calendar
- 🧠 **Agent thinking** — see the agent reason step by step in the UI
- 🤖 **Auto tool selection** — LangGraph + LLM decides which tool to use automatically
- 🦙 **Free local dev** — runs on Ollama llama3.1, zero cost, no internet needed
- ☀️🌙 **Theme toggle** — dark and light mode
- ☁️ **Production ready** — one env var switches to Anthropic Claude

---

## Live Demo

Ask the agent things like:

```
"What are my latest 5 emails?"
→ Agent calls tool_read_emails → summarizes your inbox

"Draft an email to talent@empowerpharmacy.com, subject 'Thank you', body 'Dear Team...'"
→ Agent calls tool_create_draft → creates draft in Gmail for review

"What meetings do I have this week?"
→ Agent calls tool_get_events → lists your calendar events

"Create a meeting called Standup tomorrow at 10am to 11am"
→ Agent calls tool_create_event → adds event to Google Calendar
```

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

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Language | Python 3.12 | Industry standard for AI |
| LLM (dev) | Ollama `llama3.1` | Free, offline, better tool calling |
| LLM (prod) | Anthropic `claude-sonnet-4-6` | One env var switch |
| Agent framework | LangGraph | Agent orchestration |
| Backend | FastAPI + SSE | Streaming agent thinking steps |
| Email | Gmail API | Read inbox, create drafts |
| Calendar | Google Calendar API | Read and create events |
| Auth | Google OAuth 2.0 | Secure Gmail/Calendar access |
| Frontend | React + Vite | Chat UI with theme toggle |

---

## Project Structure

```
personal-assistant-agent/
├── agent.py              # LangGraph agent brain + tool definitions
├── main.py               # FastAPI server with SSE streaming
├── gmail_tool.py         # Gmail read + draft creation
├── calendar_tool.py      # Google Calendar read + create events
├── test_agent.py         # Test all agent capabilities
├── test_gmail.py         # Test Gmail connection only
├── test_calendar.py      # Test Calendar connection only
├── requirements.txt      # Python dependencies
├── .env                  # API keys (never commit!)
├── .gitignore
└── client/               # React chat UI
    ├── index.html
    └── src/
        ├── main.jsx
        └── App.jsx       # Chat UI with thinking steps + theme toggle
```

---

## Prerequisites

- Python 3.9+
- Node.js 18+ (for React UI)
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

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install fastapi uvicorn python-dotenv \
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
# llama3.1 is recommended — better tool calling than llama3.2
ollama pull llama3.1
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

### 8. Install React dependencies
```bash
cd client
npm install
cd ..
```

---

## Running the App

You need 3 terminals:

```bash
# Terminal 1 — Ollama
ollama serve

# Terminal 2 — FastAPI backend
source venv/bin/activate
uvicorn main:app --reload

# Terminal 3 — React frontend
cd client
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Usage

### React Chat UI
Open http://localhost:5173 — click a quick prompt or type your own question.

### CLI mode
```bash
python3 test_agent.py
```

### API directly
```bash
curl "http://localhost:8000/api/ask?q=What+are+my+latest+emails"
```

### Switch to production (Anthropic Claude)
```bash
APP_ENV=production ANTHROPIC_API_KEY=sk-ant-... uvicorn main:app --reload
```

---

## Dev vs Production

| | Development | Production |
|---|---|---|
| `APP_ENV` | unset (default) | `production` |
| LLM | Ollama llama3.1 | Anthropic Claude |
| Cost | Free | Pay per token |
| Internet | Not needed | Required |

---

## Agent Thinking UI

The React UI shows the agent reasoning in real time:

```
🧠 Using tool: tool_read_emails...   ← agent decides which tool
📦 Tool result ▼                     ← raw data (click to expand)
💬 Here are your latest 5 emails...  ← final answer
```

This uses Server-Sent Events (SSE) to stream each step as it happens.

---

## Gmail Safety — Drafts Only

The agent **never sends emails directly**. It always creates drafts you review in Gmail before sending.

To send: open Gmail → Drafts → review → send manually.

**Pro tip for drafting replies:** Be explicit with the prompt:
```
Draft email to talent@company.com, subject "Re: Job Application", body "Dear Team, thank you..."
```

---

## Google OAuth Scopes

| Scope | Why |
|---|---|
| `gmail.readonly` | Read inbox and emails |
| `gmail.compose` | Create drafts |
| `calendar.readonly` | Read events |
| `calendar.events` | Create events |

---

## Why llama3.1 over llama3.2?

| Model | Size | Tool calling |
|---|---|---|
| `llama3.2` | 3B | ❌ Unreliable |
| `llama3.1` | 8B | ✅ Good |
| `mistral` | 7B | ✅ Good |
| `claude-sonnet-4-6` | — | ✅ Excellent |

Tool calling requires the model to output structured JSON that LangGraph can parse. Smaller models like llama3.2 often return raw JSON instead of executing the tool. llama3.1 at 8B handles this reliably.

---

## Important — Never Commit Secrets!

Your `.gitignore` must contain:
```
token.json
credentials.json
.env
venv/
__pycache__/
*.pyc
```

GitHub's secret scanning will block your push if these files are committed. If it happens, use `git filter-repo` to remove them from history.

---

## How the Agent Thinks

```
You ask a question
        │
        ▼
LangGraph agent receives it
        │
        ▼
LLM reads question + available tools
        │
        ▼
LLM picks the right tool
        │
        ▼
Tool calls Gmail or Calendar API
        │
        ▼
LLM reads the result
        │
        ▼
LLM decides if done or needs another tool
        │
        ▼
Streams final answer to React UI
```

---

## Roadmap

- [x] FastAPI backend
- [x] Gmail read emails
- [x] Gmail create drafts (safety first — no direct sending)
- [x] Google Calendar read events
- [x] Google Calendar create events
- [x] LangGraph agent with automatic tool selection
- [x] Streaming agent thinking steps via SSE
- [x] React chat UI with dark/light theme toggle
- [x] Ollama local dev → Claude production switch
- [ ] Web search tool
- [ ] Conversation history per session
- [ ] Deploy to production

---

## Related Project

Built as a follow-up to the [RAG Demo](https://github.com/TpPrachi/rag-demo) — a Node.js RAG system with ChromaDB, Ollama, streaming responses, and a React chat UI.

---

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

---

## License

MIT