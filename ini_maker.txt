import configparser, os

class ini_maker:
    def __init__(self):
        self.path = os.getcwd()
        
    def set_ini_value(self, file_name, title, key, new_value):
        
        '''
        有参无返
        更改配置文件内容
        参数：
            file_name：相对路径
            title：标题
            key：键
            new_value：新值
        '''

        config = configparser.ConfigParser()
        # 文件名称
        config.read(f'{self.path}\{file_name}', encoding="utf-8")

        # 如果没有这个值，就创建
        if not config.has_section(title):
            config.add_section(title)

        config.set(title, key, new_value)

        with open(f'{file_name}', 'w', encoding="utf-8") as configfile:
            config.write(configfile)


    # 获取配置项内容
            # 文件名, 标题, 键
    def get_ini_value(self, file_name, title, key):
        
        '''
        有参有返
        读取配置文件内容
        参数：
            file_name：相对路径
            title：标题
            key：键
        '''

        config = configparser.ConfigParser()
        config.read(f'{self.path}\{file_name}', encoding="utf-8")

        value = config.get(title, key)
        return value