import read_xls
from collections import defaultdict

# to = [num for num in range(5)]
# email = [num for num in range(10)]

email_dict = defaultdict(dict)

email_dict["网易"]["邮箱"] = read_xls.read_excel('wang_email.xlsx', 'email')
email_dict["网易"]["授权码"] = read_xls.read_excel('wang_email.xlsx', 'password')
email_dict["QQ"]["邮箱"] = read_xls.read_excel('qq_email.xlsx', 'email')
email_dict["QQ"]["授权码"] = read_xls.read_excel('qq_email.xlsx', 'password')
to = read_xls.read_excel('data.xlsx', 'to')

# email_dict["网易"]["邮箱"] = email_list
# email_dict["网易"]["授权码"] = email_password
# email_dict["QQ"]["邮箱"] = qq_email
# email_dict["QQ"]["授权码"] = qq_email_password


print(f"\n\n网易邮箱共有{len(email_dict['网易']['邮箱'])}个邮箱，{len(email_dict['网易']['授权码'])}条授权码\n"
      f"QQ邮箱共有{len(email_dict['QQ']['邮箱'])}个邮箱，{len(email_dict['QQ']['授权码'])}条授权码\n"
      f"共有{len(to)}个收件人\n\n")

# 邮箱计数器
email_count = 0
# 收件人计数器
to_count = 0
while (1):
    print(f"邮箱{email_dict['网易']['邮箱'][email_count]}@163.com 授权码为{email_dict['网易']['授权码'][email_count]} 向编号为 {to[to_count]} 的收件人发送了一封邮件")
    to_count += 1
    email_count += 1

    # 如果网易邮箱的邮箱第一趟跑完了还没有发完邮件，则调用qq的
    if len(email_dict["网易"]["邮箱"]) == email_count:
        email_count = 0
        # 如果qq邮箱列表不为空
        if len(email_dict["QQ"]["邮箱"]):
            while(email_dict["QQ"]["邮箱"] != email_count):
                print(f"邮箱{email_dict['QQ']['邮箱'][email_count]}@qq.com 授权码为{email_dict['QQ']['授权码'][email_count]} 向编号为 {to[to_count]} 的收件人发送了一封邮件")
                to_count += 1
                email_count += 1
                if len(email_dict["QQ"]["邮箱"]) == email_count:
                    email_count = 0
                    break

            if len(to) == to_count:
                break


    if len(to) == to_count:
        break
