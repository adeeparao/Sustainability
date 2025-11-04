import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, UTC
import sys

# Make sure we can import sustainability_agent if run from scripts folder
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from sustainability_agent import send_email  # reuse existing sender


def build_test_message() -> MIMEMultipart:
    msg = MIMEMultipart()
    sender = os.environ.get("SMTP_FROM", os.environ.get("SMTP_USER", "sustainability-agent@example.com"))
    recipient = os.environ.get("SMTP_TO", "recipient@example.com")
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = "Sustainability Agent – Test Email"
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S %Z")
    body = (
        "This is a test email from Sustainability Agent.\n\n"
        f"Timestamp: {ts}\n"
        f"From: {sender}\n"
        f"To: {recipient}\n\n"
        "If you received this message, SMTP settings are correct."
    )
    msg.attach(MIMEText(body, "plain"))
    return msg


def ensure_env_or_exit() -> None:
    required = ["SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD", "SMTP_TO"]
    missing = [k for k in required if not os.environ.get(k)]
    if missing:
        raise SystemExit(
            "Missing SMTP environment variables: " + ", ".join(missing) +
            "\nEdit scripts/""env.ps1"" and set these values, then retry."
        )


def main() -> None:
    ensure_env_or_exit()
    msg = build_test_message()
    send_email(msg)


if __name__ == "__main__":
    main()
