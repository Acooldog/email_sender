import pandas as pd

def read_excel(file_path, title) -> list:# 读取Excel文件（支持.xls和.xlsx格式）
    '''
    @param file_path: 文件路径 (str)
    @param title: 列表标题 (str)

    @return: 邮箱列表 (list)
    '''
    df = pd.read_excel(file_path, engine='openpyxl')

    # 提取email列数据（自动处理列名大小写和空格）
    email_list = df[title].tolist()  # 假设列名确实为"email"

    # 输出结果
    print("提取到的邮箱列表：")
    print(email_list)
    return email_list

# read_excel('data.xlsx', 'email')
