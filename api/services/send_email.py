import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from typing import List
from dotenv import load_dotenv
import boto3
load_dotenv()

# Email configuration
sender_email_id = os.environ.get("sender_email_id")
smtp_host = os.environ.get("smtp_host")
smtp_port = os.environ.get("smtp_port")
smtp_username = os.environ.get("smtp_username")
smtp_password = os.environ.get("smtp_password")

AWS_REGION = os.getenv('region_name')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID_S3')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_ID')
SES_SOURCE_EMAIL = os.getenv('sender_email_id')
 
ses_client = boto3.client('ses', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
 
def send_email_with_attachment(subject,body,recipients, attachment_paths):
    print("attachment_paths",attachment_paths,recipients)
    if not isinstance(recipients, str):
        recipients = ', '.join(recipients)

    if isinstance(attachment_paths, str):
        attachment_paths =[attachment_paths]
    print(recipients)
    try:
         # Replace 'your-aws-region' with your AWS region

        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] =  sender_email_id # Replace with your sender email
        message['To'] = recipients

        # message body
        part = MIMEText(body, 'html')
        message.attach(part)

        # # attachment
        # if attachment_paths:
        #     part = MIMEApplication(str.encode(attachment_string))
        # attachments
        if attachment_paths:
            for file_path in attachment_paths:
                with open(file_path, 'rb') as file:
                    part = MIMEApplication(file.read())
                part.add_header('Content-Disposition', 'attachment', filename=file_path)
                message.attach(part)

        response = ses_client.send_raw_email(
            Source=message['From'],
            Destinations=[recipients],
            RawMessage={'Data': message.as_string()}
        )
        return response


    except Exception as e:
        print("test2",e)
        return e
