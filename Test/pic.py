import cv2
import numpy as np

def get_percentage_coordinates(event, x, y, flags, param):
    """
    鼠标点击事件处理函数
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        # 获取窗口中心点
        height, width = param.shape[:2]
        center_x, center_y = width // 2, height // 2

        # 计算百分比坐标（基于窗口中心到边缘）
        percentage_x = (x - center_x) / (width / 2)
        percentage_y = (y - center_y) / (height / 2)

        # 限制百分比范围在 [-1, 1]
        percentage_x = max(-1, min(1, percentage_x))
        percentage_y = max(-1, min(1, percentage_y))

        print(f"击球点坐标: ({percentage_x:.2f}, {percentage_y:.2f})")


def main(image_path):
    # 读取图片
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法加载图像: {image_path}")
        return

    # 显示图片并绑定鼠标事件
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", get_percentage_coordinates, image)

    while True:
        cv2.imshow("Image", image)

        # 按下 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    # 替换为你的图片路径
    image_path = "./PICTURE/1.jpg"
    main(image_path)