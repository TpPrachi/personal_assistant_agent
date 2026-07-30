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
        model="llama3.2",
        temperature=0,
    )
    print("🤖 Using Ollama llama3.2 (development)")

# ── Define tools ──────────────────────────────────────────────────
@tool
def tool_read_emails(max_results: int = 5) -> str:
    """Read the latest emails from Gmail inbox."""
    emails = read_emails(max_results)
    if not emails:
        return "No emails found."
    result = ""
    for e in emails:
        result += f"From: {e['from']}\nSubject: {e['subject']}\nDate: {e['date']}\nBody: {e['body'][:200]}\n---\n"
    return result


@tool
def tool_create_draft(to: str, subject: str, body: str) -> str:
    """Create a draft email in Gmail. Never sends directly — always creates a draft for review."""
    return create_draft(to, subject, body)


@tool
def tool_get_events(days: int = 7) -> str:
    """Get upcoming calendar events for the next N days."""
    events = get_upcoming_events(days)
    if not events:
        return f"No events in the next {days} days."
    result = ""
    for e in events:
        result += f"📅 {e['title']}\n   Start: {e['start']}\n   End: {e['end']}\n"
        if e['location']:
            result += f"   📍 {e['location']}\n"
        if e['attendees']:
            result += f"   👥 {', '.join(e['attendees'])}\n"
        result += "---\n"
    return result


@tool
def tool_create_event(title: str, date: str, start_time: str, end_time: str, description: str = "", attendees: str = "") -> str:
    """Create a calendar event.

    Args:
        title: Event title
        date: Date in YYYY-MM-DD format
        start_time: Start time in HH:MM format (24hr)
        end_time: End time in HH:MM format (24hr)
        description: Optional description
        attendees: Comma separated email addresses (optional)
    """
    attendee_list = [a.strip() for a in attendees.split(",")] if attendees else []
    return create_event(title, date, start_time, end_time, description, attendee_list)


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
    prompt="""You are a helpful personal assistant with access to Gmail and Google Calendar.

You can:
- Read emails from the inbox
- Create email drafts (never send directly)
- Read upcoming calendar events
- Create new calendar events

Always be concise and helpful. When creating drafts or events, confirm what you did.
For emails, always create drafts — never send directly so the user can review first.
When asked about time, today's date context will be provided in the question."""
)


def ask_agent(question: str) -> str:
    """Send a question to the agent and get a response."""
    result = agent.invoke({
        "messages": [HumanMessage(content=question)]
    })
    return result["messages"][-1].content