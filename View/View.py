from View.MainView import Ui_HitPoint
from View.Canvas import Canvas
from PyQt5 import QtWidgets, QtCore
import sys

"""
    视图，用于显示 GUI
    @author chen
"""

class View:

    """
        初始化界面
        @param width 宽度
        @param height 高度
    """
    def __init__(self, width= 1500, height= 1000) -> None:
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainWidget = QtWidgets.QWidget()
        # 主界面
        self.ui = Ui_HitPoint()
        self.width = width
        self.height = height
        # 初始化 UI
        self.uiInit()

    """
        关闭事件
    """
    def closeEvent(self, event) -> None:
        self.app.quit()
        event.accept()

    """
        初始化 UI
    """
    def uiInit(self) -> None:
        self.ui.setupUi(self.mainWidget)
        # 加入画板
        self.canvas = Canvas(self.ui.CanvasWidget)
        # 设置布局
        CanvasLayout = QtWidgets.QVBoxLayout(self.ui.CanvasWidget)
        CanvasLayout.setContentsMargins(0, 0, 0, 0)
        CanvasLayout.addWidget(self.canvas)

        # 设置大小
        self.mainWidget.resize(self.width, self.height)
        self.mainWidget.setMinimumSize(QtCore.QSize(self.width, self.height))
        # 设置关闭事件
        self.mainWidget.closeEvent = self.closeEvent

    """
        执行
    """
    def run(self) -> None:
        self.mainWidget.show()
        sys.exit(self.app.exec_())