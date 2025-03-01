import logging
import cv2
from PyQt5.QtGui import QPainter, QPen, QPixmap, QImage
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from Utils import CoordAlgo

"""
    画板：显示图像与标记
    @author: chen
"""

class Canvas(QWidget):
    """
        初始化
        @param parent 父组件
    """
    def __init__(self, parent= None) -> None:
        super(Canvas, self).__init__(parent)
        # 矩形左上角坐标
        self.startPoint = None
        # 矩形左上角坐标，右下角坐标
        self.aimRect = None
        # 背景图片路径
        self.imagePath = None
        # 坐标生成回调函数
        self.coordCallback = None

        # 画笔颜色
        self.penSetting = (Qt.red, 4)

    """
        设置画笔
        @param color 颜色
        @param width 宽度
    """
    def setPen(self, color= Qt.red, width= 4) -> None:
        self.penSetting = (color, width)

    """
        绘制标记矩形
        @param qp QPainter
    """
    def drawAimRect(self, qp: QPainter) -> None:
        # 红色，宽度为 4 像素
        pen = QPen(*self.penSetting)
        qp.setPen(pen)
        qp.drawRect(self.aimRect[0], self.aimRect[1], self.aimRect[2] - self.aimRect[0], self.aimRect[3] - self.aimRect[1])
        # 虚线
        pen.setStyle(Qt.DashLine)
        qp.setPen(pen)
        qp.drawLine(self.aimRect[0], int((self.aimRect[1] + self.aimRect[3]) / 2), self.aimRect[2], int((self.aimRect[1] + self.aimRect[3]) / 2))

    """
        加载并绘制背景图像
        @param qp QPainter
    """
    def drawImage(self, qp: QPainter) -> None:
        # 加载图片 并 转为 RGB 格式
        image = cv2.cvtColor(cv2.imread(self.imagePath), cv2.COLOR_BGR2RGB)

        # 转换为 QImage
        height, width, channels = image.shape
        q_image = QImage(image.data, width, height, channels * width, QImage.Format_RGB888)
        qp.drawPixmap(self.rect(), QPixmap.fromImage(q_image))

    """
        设置背景
        @param imagePath 图片路径
    """
    def setImage(self, imagePath: str) -> None:
        self.imagePath = imagePath
        self.update()

    """
        重写绘制函数
    """
    def paintEvent(self, event) -> None:
        qp = QPainter()
        # 开始绘制
        qp.begin(self)

        # 绘制背景
        if self.imagePath:
            self.drawImage(qp)
        # 绘制矩形
        if self.aimRect:
            self.drawAimRect(qp)

        qp.end()

    """
        清理矩形
    """
    def cleanRect(self) -> None:
        self.aimRect = None
        self.update()

    """
        设置坐标生成回调函数
        @param callback 回调函数
    """
    def setCoordCallback(self, callback) -> None:
        self.coordCallback = callback

    """
        坐标生成函数
        @param event 事件
    """
    def createCoord(self, event) -> None:
        if not self.aimRect:
            return
        # 坐标计算
        ansX, ansY = CoordAlgo.edgePercentCoord(event.y(), event.x(), self.aimRect[1], self.aimRect[0], self.aimRect[3], self.aimRect[2])
        if abs(ansX) >= 1 or ansY >= 1 or ansY < 0:
            ansX = ansY = 0
        logging.info(f"coord: ({ansX}, {ansY})")
        if not self.coordCallback:
            return
        self.coordCallback(ansX, ansY)

    """
        鼠标点击事件
    """
    def mousePressEvent(self, event) -> None:
        # 左键 设置初始点
        if event.buttons() == Qt.LeftButton:
            self.startPoint = (event.x(), event.y())

        # 右键 生成坐标
        if event.buttons() == Qt.RightButton:
            self.createCoord(event)

    """
        鼠标移动事件
        绘制矩形
    """
    def mouseMoveEvent(self, event) -> None:
        # 只有左键点击时才有效
        if not event.buttons() == Qt.LeftButton:
            return
        self.aimRect = (self.startPoint[0], self.startPoint[1], event.x(), event.y())
        self.update()