import os
import asyncio
from email.mime.text import MIMEText
from aiosmtplib import SMTP
from langchain_core.tools import tool
from dotenv import load_dotenv


@tool("email_sender", parse_docstring=True, return_direct=True)
async def individual_email_tool(to: str, subject: str, message: str):
    """Sends email to an individual address

    Args:
        to (str): to email address
        subject (str): subject
        message (str): message of the email
    """
    load_dotenv()
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT'))
    smtp_username = os.getenv('SMTP_USERNAME')
    smtp_password = os.getenv('SMTP_PASSWORD')
    email_message = MIMEText(message)
    email_message["From"] = os.getenv('FROM_EMAIL')
    email_message["To"] = to
    email_message["Subject"] = subject
    async with SMTP(hostname=smtp_host, port=smtp_port) as smtp:
        await smtp.login(smtp_username, smtp_password)
        await smtp.send_message(email_message)