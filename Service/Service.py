import csv
import os
from copy import deepcopy

"""
    服务
    包括文件选择、读取、存储等
    @author chen
"""
class Servcie:
    STORE_NAME = "POSITION.csv"
    STORE_COLUMNS_LIST = ["xPosition", "yPosition"]

    def __init__(self) -> None:
        # 文件夹路径
        self.folderPath = None
        # 存储文件路径
        self.storeFilePath = None
        # 图片数据
        self.imageList = []
        # 图片处理进度
        self.imageIndex = 0
        # 时间戳数据
        self.timestampData = []

    """
        获取数据
        @param folderPath 文件夹路径
        @return 是否成功
    """
    def getData(self, folderPath: str) -> bool:
        # 文件夹不存在
        if not os.path.exists(folderPath):
            return False

        self.folderPath = folderPath
        # 可能的 csv 文件
        csvList = []
        # 可能的图片文件
        imageList = []
        # 获取所有文件并分类
        for filePath in os.listdir(self.folderPath):
            # 图片
            if filePath.endswith((".png", ".jpg", ".jpeg")):
                imageList.append(filePath)
            # csv
            elif filePath.endswith(".csv"):
                csvList.append(filePath)

        # 如果文件数量异常
        if not len(csvList) == 1 or len(imageList) < 1:
            return False

        # 获取时间戳数据
        timestampData = []
        with open(os.path.join(self.folderPath, csvList[0]), "r") as file:
            timestampData = list(csv.reader(file))

        # 如果时间戳与图片数量不对应
        if len(timestampData) - 1 != len(imageList):
            return False

        self.imageList = sorted(imageList, key= lambda x: int(x.split('.')[0]))
        self.timestampData = timestampData

        return True

    """
        开始处理
        @return 存储文件没有存在
    """
    def startProcess(self) -> bool:
        # 检测存储文件路径是否有效
        if not self.folderPath or os.path.exists(os.path.join(self.folderPath, Servcie.STORE_NAME)):
            return False

        self.storeFilePath = os.path.join(self.folderPath, Servcie.STORE_NAME)
        # 创建存储文件并添加属性
        with open(self.storeFilePath, "a", newline= "") as file:
            columnsList = self.timestampData[0]
            columnsList.extend(Servcie.STORE_COLUMNS_LIST)
            csv.writer(file).writerow(columnsList)
        # 下标重置
        self.imageIndex = 0

        return True

    """
        根据下标获取图像路径
        @return 图像路径
    """
    def getImagePath(self, index: int) -> str:
        if not self.imageList or index >= len(self.imageList):
            return None
        return os.path.join(self.folderPath, self.imageList[index])

    """
        保存坐标
        @param index 下标
        @param x X 坐标
        @param y Y 坐标
        @return 保存成功
    """
    def savePosition(self, index: int, x: float, y: float) -> bool:
        # 存储文件异常
        if not self.storeFilePath or not os.path.exists(self.storeFilePath):
            return False

        # 下标异常
        if index < 0 or index >= len(self.timestampData) - 1:
            return False

        with open(self.storeFilePath, "a", newline= "") as file:
            rowData = deepcopy(self.timestampData[index + 1])
            rowData.extend([x, y])
            csv.writer(file).writerow(rowData)

        return True

    """
        删除指定坐标
        @param index 数据下标
        @return 删除成功
    """
    def deletePosition(self, index: int) -> bool:
        # 存储文件异常
        if not self.storeFilePath or not os.path.exists(self.storeFilePath):
            return False

        # 下标异常
        if index < 0:
            return False

        # 读取已有数据 写入除最后的数据
        dataRecord = []
        with open(self.storeFilePath, mode= "r", newline= "") as infile:
            reader = csv.reader(infile)
            dataRecord = deepcopy(list(reader))
            lineCount = len(dataRecord)
            # 如果只剩下属性 或 下标异常
            if lineCount <= 1 or index >= lineCount - 1:
                return False

        with open(self.storeFilePath, mode= "w", newline= "") as outfile:
            writer = csv.writer(outfile)
            for i, row in enumerate(dataRecord):
                if i == index + 1:
                    continue
                writer.writerow(row)

        return True

    """
        删除存储文件
        @return 是否删除成功
    """
    def deleteStoreFile(self) -> bool:
        # 存储文件异常
        if not self.storeFilePath or not os.path.exists(self.storeFilePath):
            return False
        os.remove(self.storeFilePath)
        return True

    """
        重置
    """
    def reset(self) -> None:
        self.folderPath = None
        self.storeFilePath = None
        self.imageList = []
        self.imageIndex = 0
        self.timestampData = []