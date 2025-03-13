import sys, os,time

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from functools import partial
from collections import defaultdict, namedtuple
from itertools import cycle

from ini_maker import *
from log_maker import *

from send_email_fuc import *

from read_xls import *


log = log_maker()
# 发送邮件多线程
class send_email_thread(QThread):
    signal_send_email  = Signal(str, int)
    # 结束信号
    signal_finished = Signal(list, list)
    def __init__(self, sender, to_list, email_password, title, message, attachments=None):
        '''
        @param sender: 发件人邮箱地址
        @param to: 收件人邮箱列表 (list)
        @param email_password: 发件人邮箱授权码
        @param title: 邮件标题
        @param message: 邮件正文内容
        @param attachments: 附件路径列表（可选）
        '''
        super().__init__()

        self.send_email = send_email()
        
        self._sender = sender
        self._to_list = to_list
        self._email_password = email_password
        self._title = title
        self._message = message
        # 可为空
        self._attachments = attachments

        # 成功发送列表
        self.access_email_list = []
        # 失败发送列表
        self.fail_email_list = []

    def run(self):
        # 遍历列表开始群发
        for to in self._to_list:
            result = self.send_email.send_send_py_email(
                self._sender,
                to,
                self._email_password,
                self._title,
                self._message,
                self._attachments
            )
            # result = False

            while 1:
                # time.sleep(1)
                if result == True:
                    # log.info(f"发送邮件成功: {to}")
                    # 发送成功信号
                    self.signal_send_email.emit(to, 1)
                    self.access_email_list.append(to)
                    break
                elif result == False:
                    # log.error(f"发送邮件失败: {to}")
                    # 发送失败信号
                    self.signal_send_email.emit(to, 0)
                    self.fail_email_list.append(to)
                    break
        # 结束信号
        self.signal_finished.emit(self.access_email_list, self.fail_email_list)  

# qq发送邮件多线程
class qq_send_email_thread(QThread):
    signal_send_email  = Signal(str, int)
    # 结束信号
    signal_finished = Signal(list, list)
    def __init__(self, email_163_list, email_163_password_list, qq_list, qq_password_list, 
                 to_list, title, message, attachments=None, parent=None):
        '''
        @param email_163_list: 网易邮箱列表
        @param email_163_password_list: 网易邮箱授权码列表
        @param qq_list: qq邮箱列表
        @param qq_password_list: qq邮箱授权码列表
        @param outlook_email_list: outlook邮箱列表
        @param outlook_passwd_list: outlook邮箱授权码列表
        @param to: 收件人邮箱列表 (list)
        @param title: 邮件标题
        @param message: 邮件正文内容
        @param attachments: 附件路径列表（可选）
        '''
        super().__init__()

        self.send_email = send_email()

        self.main_window = parent

        self._email_163_list = email_163_list
        self._email_163_password_list = email_163_password_list
        self._qq_list = qq_list
        self._qq_password_list = qq_password_list
        self._to_list = to_list
        self._title = title
        self._message = message
        # 可为空
        self._attachments = attachments

        # 成功发送列表
        self.access_email_list = []
        # 失败发送列表
        self.fail_email_list = []

    def run(self):
        self.while_sender(
            wang_email=self._email_163_list,
            wang_password=self._email_163_password_list,
            qq_email=self._qq_list,
            qq_password=self._qq_password_list,
            to_list=self._to_list,
            title=self._title,
            msg=self._message,
            attachments=self._attachments
        )

    def while_sender(self, wang_email, wang_password, qq_email, qq_password, 
                     to_list, title, msg, attachments=None):
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
            print(f"延时 {self.main_window.delay_time} 秒")
            # 延迟
            time.sleep(self.main_window.delay_time)
            try:
                account = next(account_cycle)
                # 添加循环次数限制
                if idx >= len(accounts) * MAX_CYCLES:
                    raise StopIteration
                
                if "qq" in account.address:
                    result = send.qq_send_email(
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
                    result = send.send_email(
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

                print(f"邮箱{account.address} 授权码为{account.password} 向编号为 {recipient} 的收件人发送了一封邮件")

                
                while 1:
                    time.sleep(1)
                    if result == True:
                        # log.info(f"发送邮件成功: {to}")
                        # 发送成功信号
                        self.signal_send_email.emit(to, 1)
                        self.access_email_list.append(to)
                        break
                    elif result == False:
                        # log.error(f"发送邮件失败: {to}")
                        # 发送失败信号
                        self.signal_send_email.emit(to, 0)
                        self.fail_email_list.append(to)
                        break

                
            except StopIteration:
                print(f"警告：已循环发送{MAX_CYCLES}轮，停止发送")
                break

        
        self.signal_finished.emit(self.access_email_list, self.fail_email_list)  

# 一直获取布局
class get_layout_thread(QThread):
    def __init__(self, widget):
        super().__init__()
        self.main_window = widget

        self.ini = ini_maker()


    def run(self):
        while 1:
            self.main_window.create_button_group(self.ini.get_ini_value("plugins/user.ini", "email", "email_list").split(","))
            time.sleep(1)

# === 主窗口 ===
# 发送邮件主窗口
class send_main_window(QWidget):
    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_import()
        self._init_defined()
        self.window_ui()

    def _init_import(self):
        self.ini = ini_maker()

        # 最终发送的邮件列表
        self.finised_email_list = []

    def _init_defined(self):
        # 附件列表
        self.fujian_list = None
        # 网易邮箱
        self.wangyi_email = 0
        # QQ邮箱
        self.qq_email = 0

        # 网易邮箱文件路径
        self.xlsx_163_path = None
        # QQ邮箱文件路径
        self.xlsx_qq_path = None

        # 秒数设置
        self.delay_time = 5

        self.xlsx_email_list = []

    def _init_window(self):
        self.setWindowTitle(f"发送邮件")
        self.resize(650, 500)
        # 设置图标

    def window_ui(self):
        # 创建一个滚动区域
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # 确保内容可以自动调整大小

        
        # 创建一个容器小部件来放置你的布局
        container_widget = QWidget()
        container = QVBoxLayout(container_widget)

        self.link_label = QLabel()
        self.link_label.setText('使用软件之前，务必仔细阅读<a href="http://www.daoges.cn/email_sender/docs/#/" style="color: blue;">使用文档</a>')

        self.h_2025_3_4_layout = QHBoxLayout()
        self.zhankai_btn = QPushButton("点我展开高级设置")

        self.grid_window = QWidget()
        self.grid_widget = QVBoxLayout()
        # 里面的按钮布局

        # ==== set_delay_time_h_layout ====
        self.set_delay_time_h_layout = QHBoxLayout()
        self.set_delay_time_h_layout_tip = QLabel("设置发送间隔时间(为了避免被封禁, 最好5秒及以上):")
        self.set_delay_time_h_layout_tip.setFixedHeight(30)

        self.set_delay_time_line_edit = QLineEdit()
        self.set_delay_time_line_edit.setPlaceholderText("单位: 秒")
        self.set_delay_time_line_edit.setText(str(self.delay_time))

        self.set_delay_time_btn = QPushButton("设置")
        self.set_delay_time_btn.setFixedHeight(30)
        # ==== set_delay_time_h_layout ====

        # === email_list_h_layout 的提示 ===
        self.email_list_h_layout_tip = QLabel("选择带有邮箱以及授权码的xlsx文件")
        # ==== email_list_h_layout ====
        # 配置群发的邮箱列表的水平布局
        self.email_list_h_layout = QHBoxLayout()
        # 下拉框
        self.combo_box = QComboBox()
        # 添加选项到下拉框
        self.combo_box.addItem("QQ邮箱")
        self.combo_box.addItem("网易邮箱")

        # 显示选择的xlsx文件路径
        self.show_email_file_path_line_edit = QLineEdit()
        self.show_email_file_path_line_edit.setReadOnly(True)
        self.show_email_file_path_line_edit.setPlaceholderText("请选择xlsx文件")

        # 点击选择路径文件
        self.choose_email_file_path_btn = QPushButton("选择xlsx文件")

        # ==== email_list_h_layout ====
        
        # === set_to_list_h_layout_tip ====
        self.set_to_list_h_layout_tip = QLabel("选择收件人列表")
        # ==== set_to_list_h_layout ====
        # 点击获取xlsx文件的收件人列表
        self.set_to_list_h_layout = QHBoxLayout()
        self.show_to_list_line_edit = QLineEdit()
        self.show_to_list_line_edit.setReadOnly(True)
        self.show_to_list_line_edit.setPlaceholderText("请选择xlsx文件")
        self.get_xlsx_list_btn = QPushButton("点我从xlsx文件导入收件人列表")


        # 控件样式
        self.combo_box.setFixedHeight(30)
        self.combo_box.setContentsMargins(0, 10, 0, 0)
        self.get_xlsx_list_btn.setFixedHeight(30)
        self.get_xlsx_list_btn.setContentsMargins(0, 10, 0, 0)

        # ==== 水平布局 ====
        # 配置群发的邮箱列表的水平布局
        self.email_list_h_layout.addWidget(self.combo_box)
        self.email_list_h_layout.addWidget(self.show_email_file_path_line_edit)
        self.email_list_h_layout.addWidget(self.choose_email_file_path_btn)

        # 设置间隔
        self.set_delay_time_h_layout.addWidget(self.set_delay_time_h_layout_tip)
        self.set_delay_time_h_layout.addWidget(self.set_delay_time_line_edit)
        self.set_delay_time_h_layout.addWidget(self.set_delay_time_btn)

        # 选择收件人
        self.set_to_list_h_layout.addWidget(self.show_to_list_line_edit)
        self.set_to_list_h_layout.addWidget(self.get_xlsx_list_btn)

        # 窗口控件添加
        # === set_delay_time_h_layout ===
        self.grid_widget.addLayout(self.set_delay_time_h_layout)
        # === email_list_h_layout 的提示 ===
        self.grid_widget.addWidget(self.email_list_h_layout_tip)
        # === email_list_h_layout ===
        self.grid_widget.addLayout(self.email_list_h_layout)
        # self.grid_widget.addWidget(self.get_xlsx_list_btn)
        # === set_delay_time_h_layout_tip ===
        self.grid_widget.addWidget(self.set_to_list_h_layout_tip)
        # ==== set_to_list_h_layout ====
        self.grid_widget.addLayout(self.set_to_list_h_layout)

        self.grid_window.setLayout(self.grid_widget)
        # self.create_button_group(self.ini.get_ini_value("plugins/user.ini", "email", "email_list").split(","))
        # 隐藏
        self.grid_window.setVisible(False)

        # self.shuaxin = QPushButton("点我刷新收件人列表")

    
        # 邮件标题
        self.email_title = QLineEdit()
        self.email_title.setPlaceholderText("请输入邮件标题")
        self.email_title.setFixedHeight(30)
        # 样式表
        self.email_title.setStyleSheet("QLineEdit{font-size: 18px;}")

        # 文本框
        self.text_box = QTextEdit()
        self.text_box.setPlaceholderText("请输入邮件正文")
        # 设置样式表
        self.text_box.setStyleSheet("QTextEdit{font-size: 15px;}")

        # 附件选择
        self.attachments = QPushButton("附件选择(支持多个附件)")
        self.attachments.setFixedHeight(30)

        self.email_h_layout = QHBoxLayout()
        # 设置邮箱类型
        # self.wangyi_email_check_box = QCheckBox("网易邮箱")
        # self.qq_email_check_box = QCheckBox("QQ邮箱")

        # 点击发送
        self.send_btn = QPushButton("发送")
        self.send_btn.setFixedHeight(30)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)


        self.h_2025_3_4_layout.addWidget(self.zhankai_btn)

        # self.email_h_layout.addWidget(self.wangyi_email_check_box)
        # self.email_h_layout.addWidget(self.qq_email_check_box)
        self.email_h_layout.addStretch(1)

        # 将邮件卡片添加到布局中
        container.addWidget(self.link_label)
        container.addLayout(self.h_2025_3_4_layout)
        container.addWidget(self.grid_window)
        # container.addWidget(self.shuaxin)
        container.addWidget(self.email_title)
        container.addWidget(self.text_box)
        container.addLayout(self.email_h_layout)
        container.addWidget(self.attachments)
        container.addWidget(self.send_btn)
        container.addWidget(self.progress_bar)
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

        # 链接被点击
        self.link_label.linkActivated.connect(self.click_link_label)

        # 将按钮连接到槽函数
        self.zhankai_btn.clicked.connect(self.quxiao_zhankai)
        # 发送按钮
        self.send_btn.clicked.connect(self.send_email_click)
        # 附件选择
        self.attachments.clicked.connect(self.attachments_click)
        # 选中邮箱
        # self.wangyi_email_check_box.stateChanged.connect(self.wangyi_email_check_box_click)

        # ==== 高级设置中的按钮 ====
        # 下拉框切换
        self.combo_box.currentTextChanged.connect(self.on_combo_box_changed)
        # 选择xlsx文件路径
        self.choose_email_file_path_btn.clicked.connect(self.choose_email_file_path_btn_click)
        # 获取xlsx列表
        self.get_xlsx_list_btn.clicked.connect(self.get_xlsx_list_btn_click)
        # 设置秒数
        self.set_delay_time_btn.clicked.connect(self.set_delay_time_btn_click)

    # === 槽函数 ===
    # 当link链接被点击
    @Slot(str)
    def click_link_label(self, url):
        QDesktopServices.openUrl(QUrl(url))

    # 当下拉框切换时
    @Slot(str)
    def on_combo_box_changed(self, text):
        """当下拉框的选项改变时调用"""
        # print(f"当下拉框的选项改变时调用, text = {text}")
        log.info(f"当下拉框的选项改变时调用, text = {text}")
        self.show_email_file_path_line_edit.setPlaceholderText("请选择xlsx文件")
        # 如果是QQ邮箱
        if text == "QQ邮箱":
            # print("1")
            if self.xlsx_qq_path:
                # print(1.1)
                self.show_email_file_path_line_edit.setText(self.xlsx_qq_path)
            else:
                # print(1.2)
                self.show_email_file_path_line_edit.setText("请选择xlsx文件")

        # 如果是网易邮箱
        elif text == "网易邮箱":
            # print("2")
            if self.xlsx_163_path:
                # print(2.1)
                self.show_email_file_path_line_edit.setText(self.xlsx_163_path)
            else:
                # print(2.2)
                self.show_email_file_path_line_edit.setText("请选择xlsx文件")

    # 设置秒数
    @Slot()
    def set_delay_time_btn_click(self):
        '''
        设置秒数
        '''
        # 获取秒数
        second = self.set_delay_time_line_edit.text()
        # 如果秒数为空
        if not second:
            # 提示
            QMessageBox.warning(self, "警告", "请输入秒数")
            log.warning("请输入秒数")
            return
        # 如果秒数不为空
        else:
            # 提示
            QMessageBox.information(self, "提示", "设置成功")
            # 设置秒数
            self.delay_time = int(second)
            log.info(f"设置秒数成功, 秒数为: {self.delay_time}")

    # 当点击选择邮件文件路径
    @Slot()
    def choose_email_file_path_btn_click(self):
        '''
        当点击选择邮件文件路径
        '''
        # 打开文件对话框，选择xlsx文件
        file_path, _ = QFileDialog.getOpenFileName(self, "选择xlsx文件", "", "xlsx Files (*.xlsx)")
        if file_path:
            # 显示选择的文件路径
            self.show_email_file_path_line_edit.setText(file_path)
            # 保存文件路径
            if self.combo_box.currentText() == "QQ邮箱":
                self.xlsx_qq_path = file_path
            elif self.combo_box.currentText() == "网易邮箱":
                self.xlsx_163_path = file_path

    # === 非槽函数 ===
    # 添加按钮函数
    def create_button_group(self, email_list):
        '''
        添加按钮函数
        email_list: 邮件列表
        '''
        if not email_list:
            print("Error: email_list is empty or not found in the INI file.")
            return

        
        # 清空之前的按钮组
        self.clear_previous_buttons()


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

        self.grid_widget.addWidget(self.container)  # 添加到 grid_widget

    def clear_previous_buttons(self):
        '''
        清空之前的按钮组
        '''
        # 移除容器中的所有按钮
        for i in reversed(range(self.grid.count())):
            widget_to_remove = self.grid.itemAt(i).widget()
            if widget_to_remove:
                self.grid.removeWidget(widget_to_remove)
                widget_to_remove.deleteLater()

    # === 槽函数 ===
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
                        # 检查按钮是否已经被染绿
                        if btn.styleSheet() == "QPushButton { background-color: green; color: white; }":
                            # 取消绿色
                            btn.setStyleSheet("")
                            print(f"取消选择 {email}，位于第 {row + 1} 行，第 {col + 1} 列")
                            # 从 finised_email_list 中移除
                            if email in self.finised_email_list:
                                self.finised_email_list.remove(email)
                        else:
                            # 染绿按钮
                            btn.setStyleSheet("QPushButton { background-color: green; color: white; }")
                            print(f"你选择了 {email}，位于第 {row + 1} 行，第 {col + 1} 列")
                            # 添加到 finised_email_list
                            self.finised_email_list.append(email)
                        return

    # 发送邮件按钮点击事件
    @Slot()
    def send_email_click(self):
        # 网易的邮箱
        # sender = self.ini.get_ini_value("plugins/user.ini", "email", "sender")
        # email_password = self.ini.get_ini_value("plugins/user.ini", "email", "email_password")
        # # qq的邮箱
        # qq_sender = self.ini.get_ini_value("plugins/user.ini", "qq_email", "sender")
        # qq_email_password = self.ini.get_ini_value("plugins/user.ini", "qq_email", "email_password")
        
        # 发送邮件
        print("发送邮件")
        print(self.finised_email_list)
        # 如果用户选择了群发收件人
        if not len(self.xlsx_email_list)and not len(self.finised_email_list):
            log.warning("请从xlsx文件导入收件人！")
            QMessageBox.warning(self, "警告", "请从xlsx文件导入收件人！")
            return
        
        # if not len(self.finised_email_list):
        #     log.warning("未选择群发收件人")
        #     QMessageBox.warning(self, "警告", "未选择群发收件人")
        #     return
        
        if not self.xlsx_163_path and not self.xlsx_qq_path:
            log.warning("未选择xlsx文件")
            QMessageBox.warning(self, "警告", "未选择xlsx文件")
            return
        
        if not self.email_title.text():
            log.warning("请输入邮件标题")
            QMessageBox.warning(self, "警告", "请输入邮件标题")
            return

        if not self.text_box.toPlainText():
            log.warning("请输入邮件正文")
            QMessageBox.warning(self, "警告", "请输入邮件正文")
            return

        emial_163_list = read_excel(self.xlsx_163_path, "网易邮箱")
        emial_163_password_list = read_excel(self.xlsx_163_path, "网易邮箱授权码")
        qq_email_list = read_excel(self.xlsx_qq_path, "QQ邮箱")
        qq_email_password_list = read_excel(self.xlsx_qq_path, "QQ邮箱授权码")

        to_list = self.xlsx_email_list

        print("email_163_list: ", emial_163_list)
        print("email_163_password_list: ", emial_163_password_list)
        print("qq_email_list: ", qq_email_list)
        print("qq_email_password_list: ", qq_email_password_list)
        print("to_list: ", to_list)
        
        self.progress_bar.setVisible(True)
        # 设置范围
        if not len(self.finised_email_list):
            self.progress_bar.setRange(0, len(self.xlsx_email_list))
            self.progress_bar.setValue(0)
        else:
            self.progress_bar.setRange(0, len(self.finised_email_list))
            self.progress_bar.setValue(0)
        # if self.wangyi_email:
            # 开始多线程

        self.sta_send_email_thread = qq_send_email_thread(
            email_163_list=emial_163_list,
            email_163_password_list=emial_163_password_list,
            qq_list=qq_email_list,
            qq_password_list=qq_email_password_list,
            to_list=to_list,
            title=self.email_title.text(),
            message=self.text_box.toPlainText(),
            attachments=self.fujian_list,
            parent=self
        )
        self.sta_send_email_thread.signal_send_email.connect(self.send_email_down)
        self.sta_send_email_thread.signal_finished.connect(self.send_email_finished)
        self.sta_send_email_thread.start()

    # 点击从xlsx文件导入收件人列表
    @Slot()
    def get_xlsx_list_btn_click(self):
        # 打开文件对话框
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)  # 选择单个文件
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]    
            
            # 读取xlsx文件
            self.xlsx_email_list = read_excel(selected_file, "email")
            if len(self.xlsx_email_list):
                # 显示xlsx文件中的邮箱列表
                log.info(f"xlsx文件中的邮箱列表: {self.xlsx_email_list}")
                QMessageBox.information(self, "成功", f"成功导入xlsx文件中的联系人邮箱共计 {len(self.xlsx_email_list)} 条")
                self.show_to_list_line_edit.setText(selected_file)
            
            else:
                log.warning("xlsx文件中未找到email列")
                QMessageBox.warning(self, "警告", "xlsx文件中未找到email列")
                return
    
    # 点击附件选择
    @Slot()
    def attachments_click(self):
        # 打开文件对话框
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)  # 选择多个文件
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            print("选择的文件:", selected_files)
            self.fujian_list = selected_files
            self.attachments.setText(f"附件选择了 {len(selected_files)} 个")

    # 选中网易邮箱
    @Slot(int)
    def wangyi_email_check_box_click(self, state):
        if state == 2:  # 2 表示选中，0 表示未选中
            # 取消选中
            self.qq_email_check_box.setChecked(False)
            self.qq_email = 0
            # 选中
            self.wangyi_email = 1
            print(f"选中网易邮箱，网易邮箱选中状态: {self.wangyi_email} QQ邮箱选中状态: {self.qq_email}")

    # 选中QQ邮箱
    @Slot(int)
    def qq_email_check_box_click(self, state):
        if state == 2:  # 2 表示选中，0 表示未选中
            # 取消选中
            self.wangyi_email_check_box.setChecked(False)
            self.wangyi_email = 0
            # 选中
            self.qq_email = 1
            print(f"选中QQ邮箱，网易邮箱选中状态: {self.wangyi_email} QQ邮箱选中状态: {self.qq_email}")

    # 点击刷新按钮
    @Slot()
    def shuaxin_click(self):
        # 刷新按钮
        self.create_button_group(self.ini.get_ini_value("plugins/user.ini", "email", "email_list").split(","))

    # === 多线程返回信号 ===
    # 接收发送邮件返回信号
    @Slot(str, int)
    def send_email_down(self, to_email, result_int):
        '''
        收件人，结果
        result_int: 0 失败，1 成功
        '''
        if result_int:
            log.info(f"发送邮件成功: {to_email}")
            # 进度条进度加1
            self.progress_bar.setValue(self.progress_bar.value() + 1)
        
        else:
            log.error(f"发送邮件失败: {to_email}")
            # 进度条进度加1
            self.progress_bar.setValue(self.progress_bar.value() + 1)
            # QMessageBox.warning(self, "失败", f"发送给{to_email}的邮件失败")
    
    # 接收结束信号
    @Slot(list, list)
    def send_email_finished(self, access_list, fial_list):
        log.info("发送邮件完成")
        QMessageBox.information(self, "成功", f"发送邮件全部完成\n\n成功发送 {len(access_list)} 封邮件, \n失败发送 {len(fial_list)} 封邮件")
        self.progress_bar.setVisible(False)

        # 清理内存
        self.xlsx_email_list.clear()

    # 展开按钮点击事件
    @Slot()
    def quxiao_zhankai(self):
        if self.zhankai_btn.text() == "点我展开高级设置":
            self.grid_window.setVisible(True)
            self.zhankai_btn.setText("点我收起高级设置")
        else:
            self.grid_window.setVisible(False)
            self.zhankai_btn.setText("点我展开高级设置")

    @Slot()
    def on_test_button_click(self, target_row, target_col):
        """点击按钮后将 grid_layout 中指定位置的按钮变为绿色"""
        # 检查目标位置是否有效
        if target_row < self.grid.rowCount() and target_col < self.grid.columnCount():
            item = self.grid.itemAtPosition(target_row, target_col)
            if item:
                widget = item.widget()
                if isinstance(widget, QPushButton):
                    widget.setStyleSheet("QPushButton { background-color: green; color: white; }")
                else:
                    print("指定位置的项不是按钮。")
            else:
                print("指定位置为空。")
        else:
            print("指定的行或列超出范围。")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = send_main_window()
    window.show()
    sys.exit(app.exec())