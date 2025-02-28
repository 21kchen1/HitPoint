import os

"""
    路径相关的方法
    @author chen
"""

"""
        获取路径中所有文件夹路径
        @param rootPath 文件夹路径
        @return list 路径列表
    """
def getFilePaths(rootPath: str) -> list:
    filePaths = []
    # 文件夹路径与文件名
    for root, _, files in os.walk(rootPath):
        filePaths.extend([os.path.join(root, file) for file in files])
    return filePaths