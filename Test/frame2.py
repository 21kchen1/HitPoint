import sys
import cv2
from PyQt5.QtGui import QPainter, QPen, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt


class Drawing(QWidget):
    def __init__(self, parent=None):
        super(Drawing, self).__init__(parent)
        self.resize(600, 400)
        self.setWindowTitle("拖拽绘制矩形")
        self.subRect = None

    # 重写绘制函数
    def paintEvent(self, event):
        # 初始化绘图工具
        qp = QPainter()
        # 开始在窗口绘制
        qp.begin(self)
        # 加载图片
        image = cv2.imread("1.jpg")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为RGB格式

        # 转换为 QImage
        height, width, channels = image.shape
        bytes_per_line = channels * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # 转换为 QPixmap 并显示
        pixmap = QPixmap.fromImage(q_image)

        qp.drawPixmap(self.rect(), pixmap)
        # 自定义画点方法
        if self.subRect:
            self.drawRect(qp)
        # 结束在窗口的绘制
        qp.end()

    def drawRect(self, qp):
        # 创建红色，宽度为4像素的画笔
        pen = QPen(Qt.red, 4)
        qp.setPen(pen)
        qp.drawRect(*self.subRect)

    # 重写三个时间处理
    def mousePressEvent(self, event):
        print("mouse press")
        self.subRect = (event.x(), event.y(), 0, 0)

    def mouseReleaseEvent(self, event):
        print("mouse release")

    def mouseMoveEvent(self, event):
        start_x, start_y = self.subRect[0:2]
        self.subRect = (start_x, start_y, event.x() - start_x, event.y() - start_y)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = Drawing()
    demo.show()
    sys.exit(app.exec_())
