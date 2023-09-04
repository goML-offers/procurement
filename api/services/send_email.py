import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from typing import List
from dotenv import load_dotenv
load_dotenv()

# Email configuration
sender_email_id = os.environ.get("sender_email_id")
smtp_host = os.environ.get("smtp_host")
smtp_port = os.environ.get("smtp_port")
smtp_username = os.environ.get("smtp_username")
smtp_password = os.environ.get("smtp_password")


def send_email_with_attachment(subject,body,recipients, attachment_paths):
    if not isinstance(recipients, str):
        recipients = ', '.join(recipients)

    if isinstance(attachment_paths, str):
        attachment_paths =[attachment_paths]

    try:
        msg = MIMEMultipart()
        msg["From"] = sender_email_id
        msg["To"] = recipients
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))
        for attachment_path in attachment_paths:
            with open(attachment_path, "rb") as attachment:
                part = MIMEApplication(attachment.read(), Name=os.path.basename(attachment_path))
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
                msg.attach(part)

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()

        # Log in to your account
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(sender_email_id, recipients, msg.as_string())

        # Quit the server
        server.quit()

        print("Email with attachment sent successfully.")
        return 1
    except Exception as e:
        print(e)
        return e
