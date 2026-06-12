from mcp.server.fastmcp import FastMCP
from .gmail_client import (
    get_latest_emails,
    search_emails,
    get_unread_emails,
    create_draft,
    send_email
)

mcp = FastMCP("gmail-server")


@mcp.tool()
def latest_emails():
    """Get latest emails"""
    return get_latest_emails()


@mcp.tool()
def search_emails_tool(query: str):
    """Search emails using Gmail search syntax"""
    return search_emails(query)

@mcp.tool()
def get_unread_emails_tool():
    """
    Get unread emails.
    """
    return get_unread_emails()

@mcp.tool()
def create_draft_tool(
    to: str,
    subject: str,
    body: str
):
    """
    Create a Gmail draft.
    """
    return create_draft(
        to,
        subject,
        body
    )

@mcp.tool()
def send_email_tool(
    to: str,
    subject: str,
    body: str
):
    """
    Send an email.
    """
    return send_email(
        to,
        subject,
        body
    )


if __name__ == "__main__":
    mcp.run()