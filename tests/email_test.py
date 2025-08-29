import datetime
from src.utils import emailer

subject = f"群发邮箱发送功能测试 - {datetime.date.today().strftime('%Y-%m-%d')}"
body = "此处为邮箱正文。附件应包含md文件和html文件。"
md_file_path = "../outputs/daily_cv_papers.md"
html_file_path = "../outputs/electronic-paper.html"

attachments = emailer.get_attachments(md_file_path, html_file_path)
emailer.send_email(subject, body, attachments)
