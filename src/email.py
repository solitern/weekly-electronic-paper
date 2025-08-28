
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import *
import smtplib
import datetime


def send_email(md_file_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"Daily CV Papers - {datetime.date.today().strftime('%Y-%m-%d')}"

        body = "Attached is the daily summary of top Computer Vision papers from arXiv."
        msg.attach(MIMEText(body, 'plain'))

        with open(md_file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {md_file_path}")
            msg.attach(part)

        # 这里改为SSL连接
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # 使用SMTP_SSL
        server.login(SENDER_EMAIL, SENDER_PASSWORD)  # 删除ehlo()和starttls()
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Email error: {str(e)}")