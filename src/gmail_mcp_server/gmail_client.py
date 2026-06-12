from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

import base64
from email.mime.text import MIMEText
import os

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send"
]


def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    service = build(
        "gmail",
        "v1",
        credentials=creds
    )

    return service


def get_latest_emails(limit=5):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        maxResults=limit
    ).execute()

    messages = results.get("messages", [])

    email_list = []

    for msg in messages:

        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = message["payload"]["headers"]

        subject = "No Subject"
        sender = "Unknown"

        for header in headers:

            if header["name"] == "Subject":
                subject = header["value"]

            if header["name"] == "From":
                sender = header["value"]

        email_list.append({
            "from": sender,
            "subject": subject
        })

    return email_list

def search_emails(query, limit=10):
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        q=query,
        maxResults=limit
    ).execute()

    messages = results.get("messages", [])

    email_list = []

    for msg in messages:

        message = service.users().messages().get(
            userId="me",
            id=msg["id"]
        ).execute()

        headers = message["payload"]["headers"]

        subject = "No Subject"
        sender = "Unknown"

        for header in headers:

            if header["name"] == "Subject":
                subject = header["value"]

            if header["name"] == "From":
                sender = header["value"]

        email_list.append({
            "id": msg["id"],
            "from": sender,
            "subject": subject
        })

    return email_list
def get_email_content(message_id):
    service = get_gmail_service()

    message = service.users().messages().get(
        userId="me",
        id=message_id,
        format="full"
    ).execute()

    headers = message["payload"]["headers"]

    subject = "No Subject"
    sender = "Unknown"

    for header in headers:

        if header["name"] == "Subject":
            subject = header["value"]

        if header["name"] == "From":
            sender = header["value"]

    body = ""

    try:
        if "parts" in message["payload"]:

            for part in message["payload"]["parts"]:

                if part["mimeType"] == "text/plain":

                    data = part["body"]["data"]

                    body = base64.urlsafe_b64decode(
                        data
                    ).decode("utf-8")

                    break

        else:

            data = message["payload"]["body"]["data"]

            body = base64.urlsafe_b64decode(
                data
            ).decode("utf-8")

    except Exception:
        body = "Could not decode email body."

    return {
        "from": sender,
        "subject": subject,
        "body": body
    }
def get_unread_emails(limit=10):
    return search_emails("is:unread", limit)
def create_draft(to, subject, body):
    service = get_gmail_service()

    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    draft_body = {
        "message": {
            "raw": raw_message
        }
    }

    draft = service.users().drafts().create(
        userId="me",
        body=draft_body
    ).execute()

    return {
        "draft_id": draft["id"],
        "message": "Draft created successfully"
    }

def send_email(to, subject, body):
    service = get_gmail_service()

    message = MIMEText(body)

    message["to"] = to
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    sent_message = service.users().messages().send(
        userId="me",
        body={
            "raw": raw_message
        }
    ).execute()

    return {
        "message_id": sent_message["id"],
        "message": "Email sent successfully"
    }