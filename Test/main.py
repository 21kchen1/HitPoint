import sys
import cv2
import csv
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class TennisBallSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("击球点提取系统")
        self.setGeometry(100, 100, 800, 600)

        # 初始化变量
        self.image_path = None
        self.timestamp_file = None
        self.image_list = []
        self.timestamp_data = []
        self.current_image_index = 0
        self.ball_position = None

        # 创建主窗口布局
        self.create_widgets()

    def create_widgets(self):
        # 主布局
        main_layout = QVBoxLayout()

        # 照片框
        self.image_label = QLabel("照片框")
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label)

        # 按钮和输入框布局
        button_layout = QHBoxLayout()

        self.file_path_button = QPushButton("文件路径设置")
        self.file_path_button.clicked.connect(self.set_file_path)
        button_layout.addWidget(self.file_path_button)

        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_processing)
        button_layout.addWidget(self.start_button)

        self.confirm_button = QPushButton("确认")
        self.confirm_button.clicked.connect(self.confirm_position)
        button_layout.addWidget(self.confirm_button)

        self.invalid_button = QPushButton("无效")
        self.invalid_button.clicked.connect(self.mark_invalid)
        button_layout.addWidget(self.invalid_button)

        main_layout.addLayout(button_layout)

        # 坐标和张数输入框
        input_layout = QHBoxLayout()

        self.x_input = QLineEdit()
        self.x_input.setPlaceholderText("X坐标")
        input_layout.addWidget(self.x_input)

        self.y_input = QLineEdit()
        self.y_input.setPlaceholderText("Y坐标")
        input_layout.addWidget(self.y_input)

        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("张数/总数")
        input_layout.addWidget(self.count_input)

        main_layout.addLayout(input_layout)

        # 设置主窗口的中心部件
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def set_file_path(self):
        # 打开文件选择对话框
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder_path:
            self.image_path = folder_path
            self.timestamp_file = os.path.join(folder_path, "timestamps.csv")
            self.load_images_and_timestamps()

    def load_images_and_timestamps(self):
        # 加载图片和时间戳
        if not os.path.exists(self.timestamp_file):
            QMessageBox.warning(self, "错误", "时间戳文件不存在")
            return

        # 读取时间戳文件
        with open(self.timestamp_file, 'r') as f:
            reader = csv.reader(f)
            self.timestamp_data = list(reader)

        # 获取图片列表
        self.image_list = [f for f in os.listdir(self.image_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        self.image_list.sort()

        # 更新张数/总数
        self.count_input.setText(f"{0}/{len(self.image_list)}")

    def start_processing(self):
        # 开始处理图片
        if not self.image_list:
            QMessageBox.warning(self, "错误", "没有找到图片文件")
            return

        self.current_image_index = 0
        self.show_image()

    def show_image(self):
        # 显示当前图片
        if self.current_image_index >= len(self.image_list):
            QMessageBox.information(self, "提示", "所有图片已处理完成")
            return

        image_file = self.image_list[self.current_image_index]
        image_path = os.path.join(self.image_path, image_file)

        # 加载图片
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为RGB格式

        # 转换为 QImage
        height, width, channels = image.shape
        bytes_per_line = channels * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # 转换为 QPixmap 并显示
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

        # 更新张数/总数
        self.count_input.setText(f"{self.current_image_index + 1}/{len(self.image_list)}")

    def confirm_position(self):
        # 确认击球点坐标
        x = self.x_input.text()
        y = self.y_input.text()

        if not x or not y:
            QMessageBox.warning(self, "错误", "请输入X和Y坐标")
            return

        # 保存数据到 CSV 文件
        timestamp = self.timestamp_data[self.current_image_index][1]  # 假设时间戳在第二列
        with open(os.path.join(self.image_path, "ball_positions.csv"), 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.current_image_index, timestamp, x, y])

        # 加载下一张图片
        self.current_image_index += 1
        self.show_image()

    def mark_invalid(self):
        # 标记当前图片为无效
        with open(os.path.join(self.image_path, "ball_positions.csv"), 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([self.current_image_index, "无效", "", ""])

        # 加载下一张图片
        self.current_image_index += 1
        self.show_image()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TennisBallSystem()
    window.show()
    sys.exit(app.exec_())