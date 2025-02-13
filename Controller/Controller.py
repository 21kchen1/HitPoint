from Service.Service import Servcie
from View.View import View

"""
    控制器
    @author chen
"""

class Controller:
    """
        初始化
        @param view 视图
        @param service 服务
    """
    def __init__(self, view: View, service: Servcie) -> None:
        self.view = view
        self.service = service
        # 设置 view 槽
        self.setSlot()

    """
        更新进度
    """
    def updateNum(self) -> None:
        self.view.ui.NumLineEdit.setText(f" {self.service.imageIndex} / {len(self.service.imageList)} ")

    """
        设置文件夹
    """
    def selectFolder(self) -> None:
        folderPath = self.view.selectFolder()
        # 取消选择路径或异常
        if not folderPath:
            return
        if not self.service.getData(folderPath):
            self.view.folderError()
            return
        # 显示当前路径
        self.view.ui.PathLineEdit.setText(f" {folderPath} ")
        # 显示当前数量
        self.updateNum()

    """
        设置 view 各个按键槽事件
    """
    def setSlot(self) -> None:
        self.view.ui.PathButton.clicked.connect(self.selectFolder)