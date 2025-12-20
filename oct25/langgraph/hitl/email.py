import smtplib
import os
from dotenv import load_dotenv


def send_email(receiver, sender, subject, message):
    email_message = f"""\
Subject: {subject}
To: {receiver}
From: {sender}

{message}"""
    
    with smtplib.SMTP("sandbox.smtp.mailtrap.io", 2525) as server:
        load_dotenv()
        server.starttls()
        server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
        server.sendmail(sender, receiver, email_message)


if __name__ == "__main__":
    send_email("test@example.com", "sender@example.com", "Test Subject", "This is a test email.")   