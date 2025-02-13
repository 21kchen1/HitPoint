"""
    计算坐标的方法
    @author chen
"""

"""
    边缘中点为原点的百分比坐标计算
    @params aim 目标点坐标
    @params start 矩形左上角坐标
    @params end 矩形右下角坐标
    @return aim 在矩形的百分比坐标
"""
def edgePercentCoord(aimX: float, aimY: float, startX: float, startY: float, endX: float, endY: float) -> float:
    width = abs((endX - startX) / 2)
    height = abs(endY - startY)

    if width == 0 or height == 0:
        return (0, 0)

    # 计算百分比坐标
    xPercent = (aimX - startX - width) / width
    yPercent = (aimY - startY) / height

    return (xPercent, yPercent)