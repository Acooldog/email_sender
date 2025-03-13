import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate
import os
import logging

# 配置日志
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmailSender:
    def __init__(self):
        pass

    def diy_send_email(self, sender, to, email_password, title, message, attachments=None, servers=None, port=587):
        """
        发送邮件
        :param sender: 发件人邮箱地址
        :param to: 收件人邮箱地址
        :param email_password: 发件人邮箱授权码
        :param title: 邮件标题
        :param message: 邮件正文内容
        :param attachments: 附件路径列表（可选），支持多个附件
        :param servers: SMTP 服务器地址（默认为 Outlook 的 SMTP 服务器）
        :param port: 端口（默认为 587）
        """
        # 发件人邮箱地址和授权码
        sender_email = sender
        password = email_password

        # 收件人邮箱地址
        receiver_email = to

        # 设置邮件主题、发件人、收件人
        subject = title

        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg['Date'] = formatdate(localtime=True)  # 添加发送时间

        # 添加邮件正文内容
        msg.attach(MIMEText(message, 'plain'))

        # 添加附件（支持多个附件）
        if attachments:
            for attachment_path in attachments:
                try:
                    # 检查文件是否存在
                    if not os.path.isfile(attachment_path):
                        log.warning(f"附件 {attachment_path} 不存在，跳过。")
                        continue

                    with open(attachment_path, 'rb') as attachment_file:
                        part = MIMEApplication(attachment_file.read(), Name=os.path.basename(attachment_path))
                        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                        msg.attach(part)
                        log.info(f"附件 {attachment_path} 已添加到邮件中。")
                except Exception as e:
                    log.error(f"处理附件 {attachment_path} 时出错：{e}")

        # 使用SMTP服务器发送邮件
        try:
            # 如果没有指定服务器地址，则默认使用 Outlook 的 SMTP 服务器
            if not servers:
                servers = "smtp.office365.com"

            server = smtplib.SMTP(servers, port)  # Outlook SMTP 服务器地址和端口
            server.starttls()  # 启用 TLS 加密
            server.login(sender_email, password)  # 登录邮箱
            server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
            server.quit()  # 关闭连接
            log.info("邮件发送成功！")
            return True
        except Exception as e:
            log.critical(f"邮件发送失败：{e}")
            return False


# 示例用法
if __name__ == "__main__":
    email_sender = EmailSender()
    sender = "xtx666111@outlook.com"  # 发件人邮箱
    to = "2622138410@qq.com"  # 收件人邮箱
    email_password = "lpsgaaxsbxrtmmhm"  # 发件人邮箱授权码
    title = "测试邮件"
    message = "这是一封测试邮件，使用 Outlook SMTP 发送。"
    attachments = ["path/to/file1.pdf", "path/to/file2.jpg"]  # 附件路径列表

    email_sender.diy_send_email(sender, to, email_password, title, message, attachments)
