from gmail_tool import read_emails

emails = read_emails(max_results=3)
for email in emails:
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Date: {email['date']}")
    print(f"Body: {email['body'][:100]}...")
    print("---")