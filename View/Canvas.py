import cv2
from PyQt5.QtGui import QPainter, QPen, QPixmap, QImage, QPalette, QColor
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt

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
        # 背景白色
        # self.autoFillBackground()
        # palette = QPalette()
        # palette.setColor(QPalette.Window, QColor("white"))
        # self.setPalette(palette)
        # 矩形四角坐标元组
        self.subRect = None
        # 背景图片路径
        self.imagePath = None
        # 坐标生成回调函数
        self.indexCallback = None

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
    def drawsubRect(self, qp: QPainter) -> None:
        # 红色，宽度为 4 像素
        qp.setPen(QPen(*self.penSetting))
        qp.drawRect(*self.subRect)

    """
        加载并绘制背景图像
        @param qp QPainter
    """
    def drawImage(self, qp: QPainter) -> None:
        # 加载图片 并 转为 RGB 格式
        image = cv2.cvtColor(cv2.imread(self.imagePath))

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
        if self.subRect:
            self.drawsubRect(qp)

        qp.end()

    """
        设置坐标生成回调函数
        @param callback 回调函数
    """
    def setIndexCallback(self, callback) -> None:
        self.indexCallback = callback

    """
        坐标生成函数
        @param event 事件
    """
    def createIndex(self, event) -> None:
        # 坐标计算

        if not self.indexCallback:
            return
        self.indexCallback()

    """
        鼠标点击事件
    """
    def mousePressEvent(self, event) -> None:
        # 左键 设置初始点
        if event.buttons() == Qt.LeftButton:
            self.subRect = (event.x(), event.y(), 0, 0)

        # 右键 生成坐标
        if event.buttons() == Qt.RightButton:
            self.createIndex(event)

    """
        鼠标移动事件
        绘制矩形
    """
    def mouseMoveEvent(self, event) -> None:
        # 只有左键点击时才有效
        if not event.buttons() == Qt.LeftButton:
            return
        start_x, start_y = self.subRect[0:2]
        self.subRect = (start_x, start_y, event.x() - start_x, event.y() - start_y)
        self.update()