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

        # 坐标
        self.xPosition = 0
        self.yPosition = 0

        # 设置 view 槽
        self.setSlot()

    """
        更新进度信息
    """
    def updateNum(self) -> None:
        self.view.ui.NumLineEdit.setText(f" {self.service.imageIndex + 1} / {len(self.service.imageList)} ")

    """
        重置信息
        重置坐标数据
        重置视图显示
    """
    def resetData(self) -> None:
        self.xPosition = 0
        self.yPosition = 0
        self.view.cleanData()

    """
        更新坐标
        @param x X 坐标
        @param y Y 坐标
    """
    def updatePosistion(self, x: float, y: float) -> None:
        self.xPosition = x
        self.yPosition = y

        self.view.ui.XLineEdit.setText(f" {round(self.xPosition * 100, 3)}% ")
        self.view.ui.YLineEdit.setText(f" {round(self.yPosition * 100, 3)}% ")

    """
        显示图像
    """
    def showImage(self, index: int) -> None:
        image = self.service.getImagePath(index)
        if not image:
            return
        self.view.canvas.setImage(image)

    """
        设置文件夹
    """
    def selectFolder(self) -> None:
        folderPath = self.view.selectFolder()
        # 取消选择路径或异常
        if not folderPath:
            return

        # 重置
        self.service.reset()
        if not self.service.getData(folderPath):
            self.view.folderError()
            return
        # 显示当前路径
        self.view.ui.PathLineEdit.setText(f" {folderPath} ")

    """
        开始处理
    """
    def startProcess(self) -> None:
        if not self.service.startProcess():
            self.view.fileError()
            return

        self.resetData()
        self.view.RunningMode()
        # 显示第一张图片
        self.showImage(self.service.imageIndex)
        self.updateNum()

    """
        有效坐标
    """
    def validPosition(self) -> None:
        # 如果坐标无效
        if abs(self.xPosition) < 0.001 or abs(self.yPosition) < 0.001:
            self.view.positionError()
            return
        # 保存
        self.service.savePosition(self.service.imageIndex, self.xPosition, self.yPosition)
        # 数量加一
        self.service.imageIndex += 1

        # 检测是否完成
        if self.service.imageIndex >= len(self.service.imageList):
            self.finshProcess()
            return

        self.resetData()
        self.showImage(self.service.imageIndex)
        self.updateNum()

    """
        无效坐标
    """
    def invalidPosition(self) -> None:
        # 如果已经生成了坐标 且取消无效
        if abs(self.xPosition) > 0.001 and abs(self.yPosition) > 0.001 and not self.view.posistionWarning():
            return
        # 保存
        self.service.savePosition(self.service.imageIndex, 0, 0)
        # 数量加一
        self.service.imageIndex += 1

        # 检测是否完成
        if self.service.imageIndex >= len(self.service.imageList):
            self.finshProcess()
            return

        self.resetData()
        self.showImage(self.service.imageIndex)
        self.updateNum()

    """
        完成处理
    """
    def finshProcess(self) -> None:
        # 如果没有运行
        if not self.view.mode:
            return

        # 判断是否保存
        if not self.view.toSave():
            self.service.deleteStoreFile()

        # 重置
        self.resetData()
        self.service.reset()
        self.view.StandbyMode()

    """
        设置 view 各个按键槽事件
    """
    def setSlot(self) -> None:
        # 设置关闭回调函数
        self.view.setCloseCallback(self.finshProcess)
        # 设置坐标回调函数
        self.view.canvas.setCoordCallback(self.updatePosistion)
        # 设置文件夹
        self.view.ui.PathButton.clicked.connect(self.selectFolder)
        # 开始
        self.view.ui.StartButton.clicked.connect(self.startProcess)
        # 有效
        self.view.ui.ValidButton.clicked.connect(self.validPosition)
        # 无效
        self.view.ui.InvalidButton.clicked.connect(self.invalidPosition)