import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formatdate
import os
from log_maker import *
from ini_maker import *

log = log_maker()

class send_email:
    def __init__(self):
        self.ini = ini_maker()

    def send_send_py_email(self, sender, to, email_password, title, message, attachments=None):
        '''
        发送邮件 发送邮件主窗口专用
        '''
        
        return self.send_email(sender, to, email_password, title, message, attachments)

    def qq_send_email(self, sender, to, email_password, title, message, attachments=None):
        """
        发送邮件
        :param sender: 发件人邮箱地址
        :param to: 收件人邮箱地址
        :param email_password: 发件人邮箱授权码
        :param title: 邮件标题
        :param message: 邮件正文内容
        :param attachments: 附件路径列表（可选），支持多个附件
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
            server = smtplib.SMTP('smtp.qq.com', 587)  # 网易邮箱SMTP服务器地址和端口
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            log.info("邮件发送成功！")
            return True
        except Exception as e:
            log.critical(f"邮件发送失败：{e}")
            return False
    
    # 自定义发送邮件
    def diy_send_email(self, sender, to, email_password, title, message, attachments=None, servers=None, port=587):
        """
        发送邮件
        :param sender: 发件人邮箱地址
        :param to: 收件人邮箱地址
        :param email_password: 发件人邮箱授权码
        :param title: 邮件标题
        :param message: 邮件正文内容
        :param attachments: 附件路径列表（可选），支持多个附件
        :param servers: 服务器地址
        :param port: 端口 默认为587
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
            server = smtplib.SMTP(servers, port)  # 网易邮箱SMTP服务器地址和端口
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            server.quit()
            log.info("邮件发送成功！")
            return True
        except Exception as e:
            log.critical(f"邮件发送失败：{e}")
            return False

    def send_email(self, sender, to, email_password, title, message, attachments=None):
        """
        发送邮件
        :param sender: 发件人邮箱地址
        :param to: 收件人邮箱地址
        :param email_password: 发件人邮箱授权码
        :param title: 邮件标题
        :param message: 邮件正文内容
        :param attachments: 附件路径列表（可选），支持多个附件
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

        # 使用SMTP_SSL发送邮件
        try:
            context = ssl.create_default_context()  # 创建默认的SSL上下文
            with smtplib.SMTP_SSL("smtp.163.com", 465, context=context) as server:  # 使用SSL连接
                server.login(sender_email, password)  # 登录邮箱
                server.sendmail(sender_email, receiver_email, msg.as_string())  # 发送邮件
                log.info("邮件发送成功！")
                return True
        except Exception as e:
            log.critical(f"邮件发送失败：{e}")
            return False
