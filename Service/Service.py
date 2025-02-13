import csv
import os

"""
    服务
    包括文件选择、读取、存储等
    @author chen
"""
class Servcie:
    def __init__(self) -> None:
        # 文件夹路径
        self.folderPath = None
        # 图片数据
        self.imageList = []
        # 图片处理进度
        self.imageIndex = 0
        # 时间戳数据
        self.timestampData = []

    """
        获取数据
        @param folderPath 文件夹路径
    """
    def getData(self, folderPath: str) -> bool:
        # 文件夹不存在
        if not os.path.exists(folderPath):
            return False

        self.folderPath = folderPath
        # 可能的 csv 文件
        csvList = []
        # 获取所有文件并分类
        for filePath in os.listdir(self.folderPath):
            # 图片
            if filePath.endswith((".png", ".jpg", ".jpeg")):
                self.imageList.append(filePath)
            # csv
            elif filePath.endswith("csv"):
                csvList.append(filePath)

        # 如果 csv 文件数量异常
        if not len(csvList) == 1:
            return False
        # 排序图片
        self.imageList.sort()
        # 获取时间戳数据
        with open(os.path.join(self.folderPath, csvList[0]), "r") as file:
            reader = csv.reader(file)
            self.timestampData = list(reader)

        print(self.timestampData)

        return True