from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config.config import *
import smtplib


def get_attachments(md_file_path, html_file_path):
    """
        创建并返回包含附件的MIME对象列表

        Args:
            md_file_path (str): Markdown文件路径
            html_file_path (str): HTML文件路径

        Returns:
            list: 包含MIME附件对象的列表
        """
    attachments = []

    # 添加Markdown文件附件
    if md_file_path:
        with open(md_file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {md_file_path.split('/')[-1]}")
            attachments.append(part)

    # 添加HTML文件附件
    if html_file_path:
        with open(html_file_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {html_file_path.split('/')[-1]}")
            attachments.append(part)

    return attachments


def send_email(subject, body, attachments):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = ", ".join(RECEIVER_EMAILS)  # 将收件人列表转换为逗号分隔
        msg['Subject'] = subject

        body = body
        msg.attach(MIMEText(body, 'plain'))
        for attachment in attachments:
            msg.attach(attachment)

        # 这里改为SSL连接
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)  # 使用SMTP_SSL
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        # 向所有收件人发送邮件
        for receiver_email in RECEIVER_EMAILS:
            server.sendmail(SENDER_EMAIL, receiver_email, text)
        server.quit()
        print("Email sent successfully to all recipients.")
    except Exception as e:
        print(f"Email error: {str(e)}")
