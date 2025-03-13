import sys, os

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from functools import partial

from PySide6.QtWidgets import QWidget

from ini_maker import *
from log_maker import *

log = log_maker()


# 用于保存已经存在的按钮
already_save_list = []

# === 多线程 ===
# 获取所有邮件号给添加群发邮件号卡片 多线程
class get_email_in_add_email_card(QThread):
    def __init__(self, add_email_card=None):
        '''
        获取所有邮件号给添加群发邮件号卡片 多线程
        '''
        super().__init__()

        self.add_email_card = add_email_card

        self.ini = ini_maker()

    def run(self):
        # 每五个换行一次
        self.add_email_card.show_all_email_label.setText("")

        # 获取所有邮件号
        email_list = self.ini.get_ini_value("plugins/user.ini", "email", "email_list")
        # 分割
        email_list = email_list.split(",")
        # 去掉空字符串
        email_list = [email for email in email_list if email]
        # 每五个换行一次 最后一个不加符号
        self.add_email_card.show_all_email_label.setText(f"之前添加的邮件号:")
        for i in range(len(email_list)):
            if i % 5 == 0:
                self.add_email_card.show_all_email_label.setText(self.add_email_card.show_all_email_label.text() + "\n")
            self.add_email_card.show_all_email_label.setText(f"{self.add_email_card.show_all_email_label.text() + email_list[i] + '、'}")

# 获取发送者和授权码状态 多线程
class get_email_sender_and_password_thread(QThread):
    def __init__(self, set_send_to_email_card_=None):
        super().__init__()
        self.set_send_to_email_card_ = set_send_to_email_card_

        self.ini = ini_maker()

    def run(self):
        # 获取发送者和密码
        email_sender = self.ini.get_ini_value("plugins/user.ini", "email", "sender")
        email_password = self.ini.get_ini_value("plugins/user.ini", "email", "email_password")
        # 获取qq发送者和密码
        qq_email_sender = self.ini.get_ini_value("plugins/user.ini", "qq_email", "sender")
        qq_email_password = self.ini.get_ini_value("plugins/user.ini", "qq_email", "email_password")

        if email_sender == "0":
            print("email_sender 未设置")
            self.set_send_to_email_card_.show_path_input.setPlaceholderText("未设置")

        else:
            print("email_sender 已设置")
            self.set_send_to_email_card_.show_path_input.setText(email_sender)

        if email_password == "0":
            print("email_password 未设置")
            self.set_send_to_email_card_.show_password_input.setPlaceholderText("未设置")
        else:
            print("email_password 都设置了")
            self.set_send_to_email_card_.show_password_input.setText(email_password)

        # qq
        if qq_email_sender == "0":
            print("qq_email_sender 未设置")
            self.set_send_to_email_card_.qq_show_path_input.setPlaceholderText("未设置")
        else:
            print("qq_email_sender 都设置了")
            self.set_send_to_email_card_.qq_show_path_input.setText(qq_email_sender)

        if qq_email_password == "0":
            print("qq_email_password 未设置")
            self.set_send_to_email_card_.qq_show_password_input.setPlaceholderText("未设置")
        else:
            print("qq_email_password 都设置了")
            self.set_send_to_email_card_.qq_show_password_input.setText(qq_email_password)



# === 卡片 ===
# 添加群发邮件号 卡片
class add_email_card(QFrame):
    def __init__(self):
        super().__init__()
        # self.resize(500, 650)

        self.ini = ini_maker()

        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        title_layout = QHBoxLayout()
        titile_label = QLabel("添加群发邮件号")
        # 加粗
        titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        # 创建一个水平分割线
        hou_layout = QHBoxLayout()
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        # 内容
        h1_layout = QHBoxLayout()
        self.show_all_email_label = QLabel("暂时没有邮件")
        self.show_all_email_label.setVisible(False)

        self.h_2025_3_4_layout = QHBoxLayout()
        self.zhankai_btn = QPushButton("点我展开添加的邮件们")

        self.grid_window = QWidget()
        self.grid_widget = QVBoxLayout()
        self.grid_window.setLayout(self.grid_widget)
        self.create_button_group(self.ini.get_ini_value("plugins/user.ini", "email", "email_list").split(","))
        # 隐藏
        self.grid_window.setVisible(False)

        h2_layout = QHBoxLayout()
        self.add_btn = QPushButton("点我添加")
        self.add_btn.setFixedHeight(40)

        title_layout.addWidget(titile_label)
        hou_layout.addWidget(horizontal_line)
        h1_layout.addWidget(self.show_all_email_label)
        self.h_2025_3_4_layout.addWidget(self.zhankai_btn)
        h2_layout.addWidget(self.add_btn)

        container.addLayout(title_layout)
        container.addLayout(hou_layout)
        container.addLayout(h1_layout)
        container.addLayout(self.h_2025_3_4_layout)
        container.addWidget(self.grid_window)
        container.addLayout(h2_layout)
        # container.addLayout(h2_layout)

        # 将布局应用到卡片部件上

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 信号
        # 添加邮件
        self.add_btn.clicked.connect(self.add_email_btn_click)
        # 收起展开
        self.zhankai_btn.clicked.connect(self.quxiao_zhankai)

        # 设置样式表，将所有的输入框的高度都搞成40
        self.setStyleSheet("""
            QPushButton {
                min-height: 40px;
            }
            """
        )

    # === 槽函数 ===
    @Slot()
    def add_email_btn_click(self):
        # 弹出对话框
        self.add_email_dialog = AddEmailMessageBox(self)
        self.add_email_dialog.show()

    @Slot()
    def quxiao_zhankai(self):
        if self.zhankai_btn.text() == "点我展开添加的邮件们":
            self.grid_window.setVisible(True)
            self.zhankai_btn.setText("点我收起添加的邮件们")
        else:
            self.grid_window.setVisible(False)
            self.zhankai_btn.setText("点我展开添加的邮件们")

    # 添加按钮函数
    def create_button_group(self, email_list):
        '''
        添加按钮函数
        email_list: 邮件列表
        
        '''
        # email_list = self.ini.get_ini_value("plugins/user.ini", "email", "email_list")

        if not email_list:
            print("Error: email_list is empty or not found in the INI file.")
            return
        # email_list = email_list.split(",")

        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(5)

        row = col = 0
        for num, email in enumerate(email_list):
            btn = QPushButton(email)
            btn.setMinimumSize(60, 40)
            btn.clicked.connect(partial(self.on_button_click, email))
            self.grid.addWidget(btn, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

        self.grid_widget.addWidget(container)  # 添加到 grid_widget

    # 遍历按钮点击事件
    # 遍历按钮点击事件
    @Slot(str)
    def on_button_click(self, email):
        # 遍历 grid_layout 中的所有按钮，找到匹配的按钮并获取其坐标
        for row in range(self.grid.rowCount()):
            for col in range(self.grid.columnCount()):
                item = self.grid.itemAtPosition(row, col)
                if item and isinstance(item.widget(), QPushButton):
                    btn = item.widget()
                    if btn.text() == email:
                        # 从布局中移除按钮
                        self.grid.removeWidget(btn)
                        btn.deleteLater()  # 安全删除按钮
                        print(f"已删除按钮 {email}，位于第 {row + 1} 行，第 {col + 1} 列")

                        # 从配置文件中移除邮箱地址
                        self.remove_email_from_ini(email)
                        return


    def remove_email_from_ini(self, email):
        """
        从配置文件中移除指定的邮箱地址
        参数：
            email：需要移除的邮箱地址
        """
        # 配置文件路径
        config_file = "plugins/user.ini"  # 假设配置文件名为 config.ini
        section = "email"  # 配置文件中的节名
        key = "email_list"  # 配置文件中的键名

        # 使用ini_maker类操作配置文件
        ini = ini_maker()
        current_emails = ini.get_ini_value(config_file, section, key)

        # 将当前的邮箱列表分割为列表
        email_list = current_emails.split(",")

        # 移除指定的邮箱地址
        if email in email_list:
            email_list.remove(email)
            print(f"已从配置文件中移除邮箱 {email}")
        else:
            print(f"邮箱 {email} 不在配置文件中，无需移除")
            return

        # 更新配置文件中的邮箱列表
        new_email_list = ",".join(email_list)
        ini.set_ini_value(config_file, section, key, new_email_list)
        print(f"配置文件已更新，新的邮箱列表为：{new_email_list}")


# === 对话框 ===
# 添加群发邮件号 对话框
class AddEmailMessageBox(QDialog):
    def __init__(self, parent=None):
        super().__init__()

        self.main_window = parent

        self._init_window()
        self._init_import()
        self.window_ui()

    def _init_import(self):
        '''
        初始化模块
        '''
        self.ini = ini_maker()

    def _init_window(self):
        self.setWindowTitle("添加群发邮件号")
        # 无边框
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # # 置顶
        # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.resize(500, 500)

    def window_ui(self):
        # 创建滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 确保内容可以自动调整大小

        # 创建一个容器小部件来放置布局
        container_widget = QWidget()
        self.container_layout = QVBoxLayout(container_widget)  # 使用 self 以便后续访问

        # 添加初始输入框
        self.add_email_line_edit = QLineEdit()
        self.add_email_line_edit.setPlaceholderText("请输入邮箱号")
        self.container_layout.addWidget(self.add_email_line_edit)
        self.add_email_line_edit.setFixedHeight(40)

        # 添加“添加更多”按钮
        self.add_more_email_btn = QPushButton("添加更多")
        self.add_more_email_btn.setFixedHeight(40)
        self.add_more_email_btn.clicked.connect(self.add_new_email_field)
        self.container_layout.addWidget(self.add_more_email_btn)

        # 添加“完成”按钮
        self.access_btn = QPushButton("完成")
        self.access_btn.setFixedHeight(40)
        self.access_btn.clicked.connect(self.collect_emails)
        self.container_layout.addWidget(self.access_btn)

        # 设置按钮高度
        self.access_btn.setFixedHeight(40)
        self.add_more_email_btn.setFixedHeight(40)


        # 添加伸展因子
        self.container_layout.addStretch(1)

        # 将布局设置到容器小部件
        container_widget.setLayout(self.container_layout)

        # 将容器小部件设置到滚动区域
        scroll_area.setWidget(container_widget)

        # 创建主布局并添加滚动区域
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        # 设置主布局
        self.setLayout(main_layout)

        # 设置样式
        scroll_area.setStyleSheet("QScrollArea{background: transparent; border: none}")
        container_widget.setStyleSheet("QWidget{background: transparent}")


    # === 槽函数 ===
    # 添加更多按钮
    @Slot()
    def add_new_email_field(self):
        """添加新的邮箱输入框"""
        new_email_line_edit = QLineEdit()
        new_email_line_edit.setPlaceholderText("请输入邮箱号")
        self.container_layout.insertWidget(self.container_layout.count() - 3, new_email_line_edit)  # 在“添加”按钮前插入

    # 完成按钮
    @Slot()
    def collect_emails(self):
        """收集所有输入框的内容"""

        # QmessageBox确认
        reply = QMessageBox.question(self, "确认", "是否确认添加完成？", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return

        email_list = []
        for i in range(self.container_layout.count() - 2):  # 排除“添加更多”和“完成”按钮
            widget = self.container_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                email = widget.text().strip()
                if email:  # 如果输入框不为空
                    email_list.append(email)

        # 输出邮箱列表
        # print("收集到的邮箱列表:", email_list)
        log.info(f"收集到的邮箱列表: {email_list}")
        self.add_ini_email_or_get(email_list, True)

        result_text = ''
        # 每五个换一次行
        for email in email_list:
            if email in already_save_list:
                continue
            result_text += email + '、'
            # 如果取余等于0就换行
            if not email_list.index(email) % 5 and email_list.index(email) != 0:
                print("换行")
                # result_text = result_text[:-1]
                result_text += '\n'
        # 去除最后一个符号
        result_text = result_text[:-1]

        self.main_window.show_all_email_label.setText(f"{self.ini.get_ini_value('plugins/user.ini', 'email', 'email_list')}\n{result_text}")

        # 写入到ini文件

        self.close()

    
    # === 非槽函数 ===
    def add_ini_email_or_get(self, email_list=None, add_or_get=True):
        '''
        添加或获取ini文件中的邮件
        email_list: 邮件列表 获取时可为空
        add_or_get: True为添加，False为获取

        返回值:
        添加时返回True，获取时返回列表
        '''

        if not add_or_get:
            # 获取ini文件中的邮件 根据,分割
            email_list = self.ini.get_ini_value("plugins/user.ini", "email", "email_list").split(',')
            # 去除空字符串
            email_list = [i for i in email_list if i != '']
            # 去除重复的邮件
            email_list = list(set(email_list))

            log.info(f"获取到的邮箱列表: {email_list}")

            return email_list

        # 从 INI 文件中获取现有的邮箱列表
        existing_emails = self.ini.get_ini_value("plugins/user.ini", "email", "email_list")
        existing_emails_set = set(existing_emails.split(",")) if existing_emails else set()
        new_emails_set = set(email_list)

        # 找出需要添加的新邮箱
        new_emails_to_add = new_emails_set - existing_emails_set

        # 如果没有新邮箱需要添加，直接返回
        if not new_emails_to_add:
            log.info("没有新邮箱需要添加。")
            return True

        # 将新邮箱添加到现有列表中
        updated_emails = existing_emails_set.union(new_emails_to_add) if existing_emails else new_emails_to_add
        updated_emails_str = ",".join(updated_emails)

        # 写入新的邮箱列表到 INI 文件
        self.ini.set_ini_value("plugins/user.ini", "email", "email_list", updated_emails_str)

        # 在主窗口中更新按钮组
        # self.main_window.create_button_group(updated_emails_str.split(","))
        self.main_window.create_button_group(email_list)

        # 记录日志和警告
        for email in new_emails_to_add:
            log.info(f"添加了新邮箱：{email}")
        for email in new_emails_set - new_emails_to_add:
            log.warning(f"邮箱 {email} 已经存在于 INI 文件中")
            QMessageBox.warning(self, "警告", f"邮箱 {email} 已经存在")

        log.info("添加完成")
        return True

        # elif not add_or_get:
            
class set_sender_and_password_messageBox(QDialog):
    def __init__(self, text, title, key, file_path, line_edit, parent=None):
        '''
        text=要显示的文本
        title=配置文件标题头
        key=配置文件键
        file_path=配置文件路径
        line_edit=要输出的line_edit控件 int 0代表邮箱， 1代表授权码
        '''
        super().__init__()

        self.text = text
        self.title = title
        self.key = key
        self.file_path = file_path
        self.line_edit = line_edit

        self.main_window = parent

        self._init_window()
        self._init_import()
        self.window_ui()

    def _init_import(self):
        '''
        初始化模块
        '''
        self.ini = ini_maker()

    def _init_window(self):
        self.setWindowTitle(self.text)

    def window_ui(self):
        container = QVBoxLayout()

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText(self.text)
        
        btn = QPushButton("确认") 

        self.input_line.setFixedHeight(40)
        btn.setFixedHeight(40)


        container.addWidget(self.input_line)
        container.addWidget(btn)

        self.setLayout(container)

        btn.clicked.connect(self.btn_click)

    @Slot()
    def btn_click(self):
        '''
        确认按钮
        '''
        # 获取输入框的内容
        input_text = self.input_line.text()
        self.ini.set_ini_value(self.file_path, self.title, self.key, input_text)  

        QMessageBox.information(self, "提示", "设置成功")
        # 授权码
        if self.line_edit:
            self.main_window.show_password_input.setText(input_text)
        # 邮箱
        else:
            self.main_window.show_path_input.setText(input_text)

        self.close()


# 设置邮件发件人和邮箱授权码 卡片
class set_send_to_email_card(QFrame):
    def __init__(self):
        super().__init__()

        self.ini = ini_maker()
        # 多线程
        # self.get_status_thread()
        self.init_card()

    def init_card(self):
        container = QVBoxLayout()
        container.setContentsMargins(10, 10, 10, 10)
        # 设置卡片的框架形状和阴影效果
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        # 标题
        self.title_layout = QHBoxLayout()
        self.titile_label = QLabel("设置邮箱发件人、授权码")
        # 加粗
        self.titile_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        # 设置标题在垂直方向可拉伸，水平方向根据内容自适应大小
        # titile_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        hor_layout = QHBoxLayout()
        # 创建一个水平分割线
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Sunken)

        top_layout = QHBoxLayout()
        self.tishi_path_label = QLabel("邮箱发件人当前状态: ")
        self.show_path_input = QLineEdit()
        self.show_path_input.setReadOnly(True)
        self.show_path_input.setPlaceholderText("未设置")

        top_2_layout = QHBoxLayout()
        self.tishi_set_password = QLabel("邮箱授权码状态: ")
        self.show_password_input = QLineEdit()
        self.show_password_input.setReadOnly(True)
        self.show_password_input.setPlaceholderText("未设置")

        # qq邮箱发件人以及授权码状态
        top_qq_h_layout = QHBoxLayout()
        self.qq_email_path_label = QLabel("QQ邮箱发件人当前状态: ")
        self.qq_show_path_input = QLineEdit()
        self.qq_show_path_input.setReadOnly(True)
        self.qq_show_path_input.setPlaceholderText("未设置")

        top_qq_2_layout = QHBoxLayout()
        self.qq_tishi_set_password = QLabel("QQ邮箱授权码状态: ")
        self.qq_show_password_input = QLineEdit()
        self.qq_show_password_input.setReadOnly(True)
        self.qq_show_password_input.setPlaceholderText("未设置")


        # 内容
        h1_layout = QHBoxLayout()
        self.content_label = QLabel("此设置为必须设置，否则无法使用群发功能")
        self.content_label.setStyleSheet("font-size: 12px;")

        h2_layout = QHBoxLayout()
        self.git_and_gcc_path_label = QLabel("")
        # 设置路径不可见
        self.git_and_gcc_path_label.setVisible(False)
        # 设置样式表 字体颜色浅蓝色
        self.git_and_gcc_path_label.setStyleSheet("color: #0078D4;")

        h3_layout = QHBoxLayout()
        self.chose_vs_btn = QPushButton("点击设置邮箱发件人")
        self.set_password_btn = QPushButton("点击设置邮箱授权码")

        # qq邮箱发件人以及授权码状态
        h4_layout = QHBoxLayout()
        self.set_qq_email_btn = QPushButton("点击设置QQ邮箱发件人")
        self.set_qq_password_btn = QPushButton("点击设置QQ邮箱授权码")


        self.title_layout.addWidget(self.titile_label)
        hor_layout.addWidget(horizontal_line)
        top_layout.addWidget(self.tishi_path_label)
        top_layout.addWidget(self.show_path_input)
        top_layout.addStretch(1)
        top_2_layout.addWidget(self.tishi_set_password)
        top_2_layout.addWidget(self.show_password_input)
        top_2_layout.addStretch(1)
        # qq邮箱发件人以及授权码状态
        top_qq_h_layout.addWidget(self.qq_email_path_label)
        top_qq_h_layout.addWidget(self.qq_show_path_input)
        top_qq_h_layout.addStretch(1)
        top_qq_2_layout.addWidget(self.qq_tishi_set_password)
        top_qq_2_layout.addWidget(self.qq_show_password_input)
        top_qq_2_layout.addStretch(1)
        h1_layout.addWidget(self.content_label)
        h2_layout.addWidget(self.git_and_gcc_path_label)
        h3_layout.addWidget(self.chose_vs_btn)
        h3_layout.addWidget(self.set_password_btn)
        # qq邮箱发件人以及授权码状态
        h4_layout.addWidget(self.set_qq_email_btn)
        h4_layout.addWidget(self.set_qq_password_btn)
        # h3_layout.addWidget(sta_btn)

        container.addLayout(self.title_layout)
        container.addLayout(hor_layout)
        container.addLayout(top_layout)
        container.addLayout(top_2_layout)
        # qq邮箱发件人以及授权码状态
        container.addLayout(top_qq_h_layout)
        container.addLayout(top_qq_2_layout)
        container.addLayout(h1_layout)
        container.addLayout(h2_layout)
        container.addLayout(h3_layout)
        container.addLayout(h4_layout)

        # 将布局应用到卡片部件上
        self.setLayout(container)

        # 设置卡片的背景颜色
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 样式表设置QpushButton的高度都为50px
        self.setStyleSheet("QPushButton { height: 50px; }")


        # 信号
        # 点击git-bash按钮
        self.chose_vs_btn.clicked.connect(self.chose_git_path)

        # 点击授权码按钮
        self.set_password_btn.clicked.connect(self.set_password)
        # 点击qq邮箱发件人按钮
        self.set_qq_email_btn.clicked.connect(self.set_qq_email)

        # 点击qq授权码按钮
        self.set_qq_password_btn.clicked.connect(self.set_qq_password)

        self.get_email_sender_and_password_thread = get_email_sender_and_password_thread(self)
        # 启动多线程
        self.get_email_sender_and_password_thread.start()

    # === 非槽函数 ===
    # 选择目录
    @Slot()
    def chose_git_path(self):
        # 调用 QFileDialog 的 getExistingDirectory 方法来选择文件夹
        show_set_sender_box = set_sender_and_password_messageBox(
            text="请输入邮箱发件人",
            title="email",
            key="sender",
            file_path="plugins/user.ini",
            line_edit=0,
            parent=self
        )
        show_set_sender_box.show()
        show_set_sender_box.exec()

        self.get_email_sender_and_password_thread.start()

    @Slot()
    def set_password(self):
        # 获取授权码的输入框
        show_set_sender_box = set_sender_and_password_messageBox(
            text="请输入邮箱授权码",
            title="email",
            key="email_password",
            file_path="plugins/user.ini",
            line_edit=1,
            parent=self
        )
        show_set_sender_box.show()
        show_set_sender_box.exec()

        self.get_email_sender_and_password_thread.start()

    # 选择qq邮箱发件人以及授权码状态
    @Slot()
    def set_qq_email(self):
        # 获取授权码的输入框
        show_set_sender_box = set_sender_and_password_messageBox(
            text="请输入QQ邮箱发件人",
            title="qq_email",
            key="sender",
            file_path="plugins/user.ini",
            line_edit=0,
            parent=self   
        )

        show_set_sender_box.show()
        show_set_sender_box.exec()

        self.get_email_sender_and_password_thread.start()

    @Slot()
    def set_qq_password(self):
        # 获取授权码的输入框
        show_set_sender_box = set_sender_and_password_messageBox(
            text="请输入QQ邮箱授权码",
            title="qq_email",
            key="email_password",
            file_path="plugins/user.ini",
            line_edit=1,
            parent=self   
        )
        show_set_sender_box.show()
        show_set_sender_box.exec()

        self.get_email_sender_and_password_thread.start()




# === 主窗口 ===
class setting_main_window(QWidget):
    def __init__(self):
        super().__init__()
        self._init_window()
        self.window_ui()

    def _init_window(self):
        self.setWindowTitle(f"设置")
        self.setFixedSize(650, 500)
        # 设置图标

    def window_ui(self):
        # 创建一个滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 确保内容可以自动调整大小

        # 创建一个容器小部件来放置你的布局
        container_widget = QWidget()
        container = QVBoxLayout(container_widget)

        # 添加群发邮件卡片
        self.add_email = add_email_card()
        # 创建设置邮件发件人、授权码卡片
        self.set_send_to_email_card = set_send_to_email_card()

        self.add_email.setContentsMargins(50, 25, 50, 0)
        self.set_send_to_email_card.setContentsMargins(50, 25, 50, 0)

        # 将邮件卡片添加到布局中
        container.addWidget(self.add_email)
        container.addWidget(self.set_send_to_email_card)
        container.addStretch(1)

        # 将布局设置到容器小部件
        container_widget.setLayout(container)

        # 将容器小部件设置到滚动区域
        scroll_area.setWidget(container_widget)

        # 创建主布局并添加滚动区域
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)

        # 设置主布局
        self.setLayout(main_layout)

        scroll_area.setStyleSheet("QScrollArea{background: transparent; border: none}")
        container_widget.setStyleSheet("QWidget{background: transparent}")

        # 启动多线程
        # self.run_get_email_in_add_email_card_thread()


    # === 多线程函数 ===
    # 获取所有邮件号给添加群发邮件号卡片 多线程
    def run_get_email_in_add_email_card_thread(self):
        '''
        获取所有邮件号给添加群发邮件号卡片 多线程
        '''
        self.get_email_in_add_email_card_thread = get_email_in_add_email_card(self.add_email)
        self.get_email_in_add_email_card_thread.start()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = setting_main_window()
    window.show()
    sys.exit(app.exec())