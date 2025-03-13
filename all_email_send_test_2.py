from collections import defaultdict, namedtuple
from itertools import cycle
# import read_xls
from send_email_fuc import *


def while_sender(wang_email, wang_password, qq_email, qq_password, to_list, title, msg, attachments=None):
    '''
    @brief 加特林发送邮件

    wang_email: 网易邮箱列表
    wang_password: 网易邮箱授权码列表
    qq_email: qq邮箱列表
    qq_password: qq邮箱授权码列表
    to_list: 收件人列表
    title: 邮件标题
    msg: 邮件内容
    attachments: 附件列表 (可选)
    '''

    send = send_email()
    # 初始化数据结构
    email_dict = defaultdict(dict)

    # 读取数据时过滤空值
    # email_dict["网易"]["邮箱"] = [e for e in read_xls.read_excel('wang_email.xlsx', '网易邮箱') if e and e != "nan"]
    # email_dict["网易"]["授权码"] = [p for p in read_xls.read_excel('wang_email.xlsx', '网易邮箱授权码') if p and p != "nan"]
    # email_dict["QQ"]["邮箱"] = [e for e in read_xls.read_excel('qq_email.xlsx', 'email') if e and e != "nan"]
    # email_dict["QQ"]["授权码"] = [p for p in read_xls.read_excel('qq_email.xlsx', 'password') if p and p!= "nan"]
    email_dict["网易"]["邮箱"] = wang_email
    email_dict["网易"]["授权码"] = wang_password
    email_dict["QQ"]["邮箱"] = qq_email
    email_dict["QQ"]["授权码"] = qq_password
    to = to_list

    # 数据校验
    for provider in ["网易", "QQ"]:
        if len(email_dict[provider]["邮箱"]) != len(email_dict[provider]["授权码"]):
            raise ValueError(f"{provider}邮箱与授权码数量不匹配")

    # 构建账户列表（不再拼接域名）
    EmailAccount = namedtuple("EmailAccount", ["address", "password"])
    accounts = []
    for provider in ["网易", "QQ"]:
        if email_dict[provider]["邮箱"]:
            accounts.extend([
                EmailAccount(e, p) 
                for e, p in zip(email_dict[provider]["邮箱"], email_dict[provider]["授权码"])
            ])

    account_cycle = cycle(accounts)

    # 发送邮件主逻辑
    MAX_CYCLES = len(to)  # 最大循环次数
    for idx, recipient in enumerate(to):
        try:
            account = next(account_cycle)
            # 添加循环次数限制
            if idx >= len(accounts) * MAX_CYCLES:
                raise StopIteration
            print(f"邮箱{account.address} 授权码为{account.password} 向编号为 {recipient} 的收件人发送了一封邮件")
            if "qq" in account.address:
                send.qq_send_email(
                    # 发件人
                    account.address,
                    # 收件人
                    recipient,
                    # 授权码
                    account.password,
                    # 标题
                    title,
                    # 内容
                    msg,
                    # 附件 (可选)
                    attachments
                )
            elif "163" in account.address:
                send.send_email(
                    # 发件人
                    account.address, 
                    # 收件人
                    recipient,
                    # 授权码
                    account.password,
                    # 标题
                    title,
                    # 内容
                    msg,
                    # 附件 (可选)
                    attachments
                )
        except StopIteration:
            print(f"警告：已循环发送{MAX_CYCLES}轮，停止发送")
            break