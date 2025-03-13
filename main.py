from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from main_window import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec())