# Personal Assistant Agent 🤖

A Python-based AI agent that connects to your Gmail and Google Calendar. Ask it anything in plain English — it figures out which tool to use and gets it done.

> Built to learn Python, FastAPI, LangGraph, and AI agents — coming from a Node.js + RAG background.

---

## What it does

- 📧 **Read emails** — fetch and summarize your latest inbox
- 📝 **Draft emails** — agent creates drafts, never sends directly (safety first)
- 📅 **Check calendar** — see upcoming events and meetings
- 🤖 **Agent brain** — Claude decides which tool to use based on your question
- ⚡ **Streaming responses** — answers appear word by word
- 💬 **React chat UI** — same stack as the RAG project

---

## How agents work vs RAG

```
RAG:    Question → Search docs → Answer

Agent:  Question → Think → Pick tool → Use it → Think again → Answer
                    ↑___________________________________|
                         (loops until task is done)
```

The agent reasons in a loop, using tools like Gmail and Calendar until it completes the task.

---

## Tech Stack

| Layer | Tool | Why |
|---|---|---|
| Language | Python 3.9+ | Industry standard for AI |
| LLM | Anthropic Claude | Powers the agent brain |
| Agent framework | LangGraph | Agent orchestration, extremely hot right now |
| Backend | FastAPI | Python equivalent of Express.js |
| Email | Gmail API | Read inbox, create drafts |
| Calendar | Google Calendar API | Read and create events |
| Frontend | React + Vite | Chat UI |
| Auth | Google OAuth 2.0 | Secure Gmail/Calendar access |

---

## Project Structure

```
personal-agent/
├── main.py               # FastAPI server
├── gmail_tool.py         # Gmail read + draft creation
├── calendar_tool.py      # Google Calendar read + create events
├── agent.py              # LangGraph agent brain
├── test_gmail.py         # Test Gmail connection
├── test_calendar.py      # Test Calendar connection
├── credentials.json      # Google OAuth credentials (never commit!)
├── token.json            # Auto-generated auth token (never commit!)
├── .env                  # API keys (never commit!)
├── .gitignore
├── requirements.txt
└── client/               # React chat UI
    ├── index.html
    └── src/
        ├── main.jsx
        └── App.jsx
```

---

## Prerequisites

- Python 3.9+
- Node.js 18+ (for React UI)
- Anthropic API key
- Google Cloud project with Gmail + Calendar APIs enabled

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/TpPrachi/personal-agent.git
cd personal-agent
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn anthropic python-dotenv \
  google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### 4. Set up environment variables
```bash
touch .env
```
Add to `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### 5. Set up Google OAuth

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project called `personal-agent`
3. Enable **Gmail API** and **Google Calendar API**
4. Go to **APIs & Services → Credentials → Create Credentials → OAuth Client ID**
5. Application type: **Desktop App**
6. Download JSON → save as `credentials.json` in project root
7. Go to **OAuth Consent Screen → Audience → Test Users**
8. Add your Gmail address as a test user

### 6. Authenticate with Google
```bash
python3 test_gmail.py
```
A browser window opens → log in → allow permissions → `token.json` is saved automatically.

### 7. Run the server
```bash
uvicorn main:app --reload
```

---

## Usage

### Test Gmail connection
```bash
python3 test_gmail.py
```

### Ask the agent anything
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are my latest emails?"}'
```

### Run React UI
```bash
cd client
npm install
npm run dev
```
Open **http://localhost:5173**

---

## Gmail Safety — Drafts Only

The agent **never sends emails directly**. It always creates drafts that you can review in Gmail before sending. This is intentional — you stay in control.

```python
# The agent calls this — creates a draft, never sends
def create_draft(to, subject, body):
    ...
```

To send a draft: open Gmail → Drafts → review → send manually.

---

## Google OAuth Scopes

| Scope | Why |
|---|---|
| `gmail.readonly` | Read inbox and emails |
| `gmail.compose` | Create drafts |
| `calendar.readonly` | Read events (coming soon) |
| `calendar.events` | Create events (coming soon) |

---

## How the Agent Works

```
You: "Draft an email to john@email.com about the project update"
           │
           ▼
    Claude reads your message
           │
           ▼
    Picks the right tool → create_draft
           │
           ▼
    Calls create_draft(to, subject, body)
           │
           ▼
    Draft appears in your Gmail
           │
           ▼
    Agent reports back: "✅ Draft created!"
```

---

## Roadmap

- [x] FastAPI backend
- [x] Claude integration
- [x] Gmail read emails
- [x] Gmail create drafts (safety first — no direct sending)
- [ ] Google Calendar read events
- [ ] Google Calendar create events
- [ ] LangGraph agent with tool selection
- [ ] React chat UI
- [ ] Streaming responses
- [ ] Deploy to production

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

---

## Related Project

This project is a continuation of the [RAG Demo](https://github.com/TpPrachi/rag-demo) — a Node.js RAG system with ChromaDB, Ollama, streaming responses and a React chat UI.

## License

MIT