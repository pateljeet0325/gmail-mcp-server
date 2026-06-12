from src.gmail_mcp_server.gmail_client import get_latest_emails

emails = get_latest_emails()

for email in emails:
    print(email)