# agent.py
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from gmail_tool import read_emails, create_draft
from calendar_tool import get_upcoming_events, create_event

load_dotenv()

# ── Switch between Ollama (dev) and Claude (prod) ─────────────────
ENV = os.getenv("APP_ENV", "development")

if ENV == "production":
    from langchain_anthropic import ChatAnthropic
    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )
    print("🤖 Using Claude (production)")
else:
    from langchain_ollama import ChatOllama
    llm = ChatOllama(
        # model="llama3.2",
        # model="mistral",
        model="llama3.1",
        temperature=0,
    )
    # print("🤖 Using Ollama llama3.2 (development)")
    # print("🤖 Using Ollama mistral (development)")
    print("🤖 Using Ollama llama3.1 (development)")

# ── Define tools ──────────────────────────────────────────────────
@tool
def tool_read_emails(max_results: int = 5) -> str:
    """Read latest emails from Gmail."""
    ...

@tool
def tool_create_draft(to: str, subject: str, body: str) -> str:
    """Create a Gmail draft. Args: to=email address, subject=subject line, body=email text."""
    ...

@tool
def tool_get_events(days: int = 7) -> str:
    """Get upcoming Google Calendar events."""
    ...

@tool
def tool_create_event(title: str, date: str, start_time: str, end_time: str, description: str = "", attendees: str = "") -> str:
    """Create a Google Calendar event. Date format: YYYY-MM-DD. Time format: HH:MM."""
    ...

# ── Create agent ──────────────────────────────────────────────────
tools = [
    tool_read_emails,
    tool_create_draft,
    tool_get_events,
    tool_create_event,
]

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt="""You are a personal assistant. Use tools to help with emails and calendar.

Rules:
- ALWAYS use a tool to answer. Never guess.
- For emails: use tool_read_emails
- For drafts: use tool_create_draft  
- For calendar: use tool_get_events
- For new events: use tool_create_event"""
)


def ask_agent(question: str) -> str:
    """Send a question to the agent and get a response."""
    result = agent.invoke({
        "messages": [HumanMessage(content=question)]
    })
    return result["messages"][-1].content