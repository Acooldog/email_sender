import sys, os

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


from send import *
from setting import *

# from pai_ping import *

# 主窗口
class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 服务器验证
        self.server_num = 0
        # 必须进行更新
        self.update_must = 0
        # 登录
        # self.run_auto_login()
        self._init_window()
        self.window_ui()

    def _init_window(self):
        self.setWindowTitle(f"道哥群发邮件工具V1.2.0")
        # self.resize(1000, 800)
        # 设置图标
        self.setWindowIcon(QIcon("plugins/daoges.ico"))
        self.resize(600, 550)

    def window_ui(self):

        container = QVBoxLayout(self)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建工具栏（导航栏）
        toolbar = QToolBar("导航栏")
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # 创建堆叠式窗口部件来管理页面
        self.stacked_widget = QStackedWidget()
        self.page1 = send_main_window()
        self.page2 = setting_main_window()
        self.setting = QLabel("设置界面")
        # self.kaiuan = kaiyuanInterface(self)
        self.stacked_widget.addWidget(self.page1)
        self.stacked_widget.addWidget(self.page2)
        self.stacked_widget.addWidget(self.setting)
        # self.stacked_widget.addWidget(self.kaiuan)
        # layout.addWidget(self.stacked_widget)

        # 创建导航按钮并添加到工具栏
        button1 = QPushButton("群发界面")
        button1.clicked.connect(self.show_page1)
        toolbar.addWidget(button1)

        button2 = QPushButton("设置界面")
        button2.clicked.connect(self.show_page2)
        toolbar.addWidget(button2)

        # setting_btn = QPushButton("设置界面")
        # setting_btn.clicked.connect(self.show_setting)
        # toolbar.addWidget(setting_btn)

        # kaiyuan_btn = QPushButton("开源协议")
        # kaiyuan_btn.clicked.connect(self.show_kaiyuan)
        # toolbar.addWidget(kaiyuan_btn)

        container.addWidget(self.stacked_widget)

        central_widget.setLayout(container)

    # === 槽函数 ===
    def show_page1(self):
        self.stacked_widget.setCurrentIndex(0)

    def show_page2(self):
        self.stacked_widget.setCurrentIndex(1)

    def show_setting(self):
        self.stacked_widget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec())