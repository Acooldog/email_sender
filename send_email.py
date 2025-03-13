
import smtplib, configparser, os, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 登录发送邮件
class login_send_email():
    def __init__(self):
        super().__init__()
        self.path = os.getcwd()
        # ini = self.get_ini_value(r'\plugins\cdkey.ini', 'CHECK', 'cdkey')

        self._init_defined()

    # 初始化变量以及判断
    def _init_defined(self):
        # 身份证
        self.id_card = self.get_ini_value("plugins/user.ini", "login", "id_code")
        # 姓名
        self.name = self.get_ini_value("plugins/user.ini", "login", "name")

        # 判断gitbash和gcc设置路径没有
        self.git = self.get_ini_value("plugins/user.ini", "path", "gitbash")
        self.gcc = self.get_ini_value("plugins/user.ini", "path", "gcc")
        if self.git == "0" and self.gcc == "0":
            self.git_and_gcc = "用户没设置gitbash和gcc的路径"
        elif self.git == "0":
            self.git_and_gcc = "用户没设置gitbash的路径"
        elif self.gcc == "0":
            self.git_and_gcc = "用户没设置gcc的路径"
        else:
            self.git_and_gcc = "用户设置了gitbash和gcc的路径"


    # 手动登录方法
    def login_sender(self, name, code):
        self.send_email(
            "yxbb110621@gmail.com",
            "2622138410@qq.com",
            "pqzxuqyifqtxicaj",
            '用户手动登录',
            f'管理员你好!\n\n姓名: {name} 的用户手动登录了软件\n\n他的账号: {code}\n\n他的路径设置情况: {self.git_and_gcc}\n\n请及时核查该用户是否具有使用权限! '
        )
        print("发送 手动登录方法邮件 完成! ")

    # 自动登录方法
    def auto_login_sender(self):
        self.send_email(
            "1503250071@qq.com",
            "2622138410@qq.com",
            "pqzxuqyifqtxicaj",
            '用户自动登录',
            f'管理员你好!\n\n姓名: {self.name} 的用户自动登录了软件\n\n他的账号: {self.id_card}\n\n他的路径设置情况: {self.git_and_gcc}\n\n请及时核查该用户是否具有使用权限!'
        )
        print("发送 自动登录方法邮件 完成! ")
    
    # 尝试手动登录失败方法
    def try_login_sender(self, name=None, text=None):
        '''
        尝试手动登录但是失败的调用方法
        参数: name可空
        参数: text可空
        发送邮件
        '''
        self.send_email(
            "1503250071@qq.com",
            "2622138410@qq.com",
            "pqzxuqyifqtxicaj",
            '用户尝试手动登录, 但手动登录失败',
            f"尝试手动登录用户姓名: {name}\n\n失败具体原因: {text}"
        )
        print("发送 尝试手动登录失败方法邮件 完成! ")

    # 尝试自动登录失败方法
    def try_auto_login_sender(self, name=None, text=None):
        '''
        尝试自动登录但是失败的调用方法
        参数: name可空
        参数: text可空
        发送邮件
        '''
        self.send_email(
            "1503250071@qq.com",
            "2622138410@qq.com",
            "pqzxuqyifqtxicaj",
            '用户尝试自动登录, 但自动登录失败',
            f"尝试自动登录用户姓名: {name}\n\n失败具体原因: {text}"
        )
        print("发送 尝试自动登录失败方法邮件 完成! ")

    # 发生错误邮件
    def error_sender(self, text=None):
        '''
        发生错误的调用方法
        参数: text可空
        发送邮件
        '''
        self.send_email(
            "1503250071@qq.com",
            "2622138410@qq.com",
            "pqzxuqyifqtxicaj",
            '用户使用软件发生严重错误!',
            f"\n\n失败具体原因: {self.name} 尝试 {text}\n\n请及时核查该用户是否在想方设法使用非法手段使用软件!"
        )

    # 发送邮件
        # 发件人   收件人  授权码  标题  内容
    def send_email(self, sender, to, email_password, title, meg):
        # 发件人邮箱地址和授权码
        sender_email = sender
        password = email_password

        # 收件人邮箱地址
        receiver_email = to

        # 设置邮件主题、发件人、收件人
        subject = title
        message = meg

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # 添加邮件正文内容
        msg.attach(MIMEText(message, 'plain'))

        # 使用QQ邮箱的SMTP服务器发送邮件
        try:
            server = smtplib.SMTP('smtp.163.com', 465)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print("邮件发送成功！")
        except Exception as e:
            print(f"邮件发送失败：{e}")

    # 获取配置项内容
            # 文件名, 标题, 键
    def get_ini_value(self, file_name, title, key):
        config = configparser.ConfigParser()
        config.read(f'{self.path}\{file_name}', encoding='utf-8')

        value = config.get(title, key)
        return value
