from View.MainUi import Ui_HitPoint
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
        # 关闭回调函数
        self.closeCallback = None
        # 运行模式 false 待机 true 运行
        self.mode = False
        # 初始化 UI
        self.uiInit()

    """
        设置关闭回调函数
        @param callback 回调函数
    """
    def setCloseCallback(self, callback) -> None:
        self.closeCallback = callback

    """
        关闭事件
    """
    def closeEvent(self, event) -> None:
        if self.closeCallback:
            self.closeCallback()
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
        # 待机模式
        self.StandbyMode()

    """
        视图待机模式
        允许使用 Path 部分
        禁止使用 Judge 部分
    """
    def StandbyMode(self) -> None:
        self.ui.MeauPath.setEnabled(True)
        self.ui.MeauJudge.setEnabled(False)
        self.mode = False

    """
        视图运行模式
        允许使用 Judge 部分
        禁止使用 Path 部分
    """
    def RunningMode(self) -> None:
        self.ui.MeauPath.setEnabled(False)
        self.ui.MeauJudge.setEnabled(True)
        self.mode = True

    """
        清除数据信息
        包括坐标, 进度与绘制内容
    """
    def cleanData(self) -> None:
        self.canvas.cleanRect()
        self.canvas.setImage(None)
        self.ui.XLineEdit.setText("")
        self.ui.YLineEdit.setText("")
        self.ui.NumLineEdit.setText("")

    """
        文件夹路径设置
    """
    def selectFolder(self) -> str:
        return QtWidgets.QFileDialog.getExistingDirectory(self.mainWidget, "Select Folder")

    """
        文件夹错误
    """
    def folderError(self) -> None:
        QtWidgets.QMessageBox.critical(self.mainWidget, "Error", "Folder exception.")

    """
        文件异常
    """
    def fileError(self) -> None:
        QtWidgets.QMessageBox.critical(self.mainWidget, "Error", "No folder has been selected or store file already exists.")

    """
        坐标异常
    """
    def positionError(self) -> None:
        QtWidgets.QMessageBox.critical(self.mainWidget, "Error", "Please enter valid coordinates.")

    """
        保存坐标文件
        @return 是否保存
    """
    def toSave(self) -> bool:
        return QtWidgets.QMessageBox.Yes == QtWidgets.QMessageBox.question(self.mainWidget, "Save Position File", "Whether to save a coordinate file?",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

    """
        舍弃坐标警告
        @return 是否舍弃
    """
    def posistionWarning(self) -> bool:
        return QtWidgets.QMessageBox.Yes == QtWidgets.QMessageBox.question(self.mainWidget, "Warning", "Are you sure to discard the coordinates?",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

    """
        执行
    """
    def run(self) -> None:
        self.mainWidget.show()
        sys.exit(self.app.exec_())