# test_agent.py
from agent import ask_agent

print("🤖 Testing agent...\n")

# Test 1: Read emails
print("Test 1: Read emails")
print(ask_agent("What are my latest 3 emails?"))
print()

# Test 2: Check calendar
print("Test 2: Check calendar")
print(ask_agent("What meetings do I have in the next 3 days?"))
print()

# Test 3: Create a draft
print("Test 3: Create draft email")
print(ask_agent("Draft an email to test@example.com with subject 'Hello' and body 'This is a test from my AI agent!'"))
print()

# Test 4: Create calendar event
print("Test 4: Create calendar event")
print(ask_agent("Create a calendar event called 'Agent Test Meeting' tomorrow from 2pm to 3pm"))
print()