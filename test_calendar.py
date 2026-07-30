# test_calendar.py
from calendar_tool import get_upcoming_events, create_event
from datetime import datetime, timedelta

# Test 1: Read upcoming events
print("📅 Upcoming events:")
events = get_upcoming_events(days=7)
if events:
    for event in events:
        print(f"  → {event['title']}")
        print(f"     Start: {event['start']}")
        print(f"     End:   {event['end']}")
        if event['location']:
            print(f"     📍 {event['location']}")
        if event['attendees']:
            print(f"     👥 {', '.join(event['attendees'])}")
        print()
else:
    print("  No upcoming events found")

# Test 2: Create a test event
print("📝 Creating test event...")
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
result = create_event(
    title="Test Event from Agent",
    date=tomorrow,
    start_time="10:00",
    end_time="11:00",
    description="Created by my personal assistant agent!"
)
print(result)