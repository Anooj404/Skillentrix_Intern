import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

SENDER_MAIL = os.getenv("SENDER_MAIL")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_MAIL = os.getenv("RECEIVER_MAIL")

def send_mail(subject: str, body: str, attach_report: bool = False) -> None:
    """
    Send an email notification for the ETL pipeline.

    If attach_report is True, attach the generated PDF report.
    """
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["from"] = SENDER_MAIL
    msg["to"] = RECEIVER_MAIL
    msg.set_content(body)
    if attach_report:
        with open("reports/ETL_Report.pdf","rb") as file:
            report = file.read()
            msg.add_attachment(
            report,
            maintype="application",
            subtype="pdf",
            filename="ETL_Report.pdf"
        )
    
    with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
        smtp.login(SENDER_MAIL, EMAIL_PASSWORD)
        smtp.send_message(msg)

        
    