"""
车牌配置常量

定义中国车牌生成器所需的所有常量配置
"""

from typing import List
from enum import Enum


# ============== 车牌类型常量 ==============

class PlateLength:
    """车牌长度"""
    NORMAL = 7  # 普通车牌7位
    NEW_ENERGY = 8  # 新能源车牌8位

# 兼容旧代码
PLATE_LENGTH_NORMAL = PlateLength.NORMAL
PLATE_LENGTH_NEW_ENERGY = PlateLength.NEW_ENERGY


class PlateHeight:
    """车牌高度（像素）"""
    SINGLE = 140  # 单层
    DOUBLE = 220  # 双层


class PlateWidth:
    """车牌宽度（像素）"""
    CHARS_7 = 440  # 7位字符
    CHARS_8 = 480  # 8位字符（新能源）


# ============== 字符宽度配置 ==============

class FontWidth:
    """字符宽度（像素）"""
    NORMAL = 45  # 普通车牌
    NEW_ENERGY = 43  # 新能源车牌
    DOUBLE = 65  # 双层车牌


# ============== 字符间隔配置 ==============

class StepSplit:
    """螺栓间隔（像素）"""
    NORMAL_7 = 34  # 7位车牌
    NEW_ENERGY_8 = 49  # 8位车牌


class StepFont:
    """字符间隔（像素）"""
    NORMAL_7 = 12  # 7位车牌
    NEW_ENERGY_8 = 9  # 8位车牌
    DOUBLE = 15  # 双层车牌


# ============== 车牌颜色 ==============

class PlateColor(Enum):
    """车牌颜色枚举"""
    BLUE = "blue"  # 普通轿车
    YELLOW = "yellow"  # 中型车
    GREEN_CAR = "green_car"  # 新能源轿车
    GREEN_TRUCK = "green_truck"  # 新能源卡车
    WHITE = "white"  # 白色警车
    WHITE_ARMY = "white_army"  # 白色军车
    BLACK = "black"  # 粤港澳
    BLACK_SHI = "black_shi"  # 使领馆


# ============== 省份代码 ==============

PROVINCES: List[str] = [
    "京", "津", "冀", "晋", "蒙", "辽", "吉", "黑", "沪",
    "苏", "浙", "皖", "闽", "赣", "鲁", "豫", "鄂", "湘",
    "粤", "桂", "琼", "渝", "川", "贵", "云", "藏", "陕",
    "甘", "青", "宁", "新"
]


# ============== 字符集 ==============

DIGITS: List[str] = [str(x) for x in range(1, 10)] + ['0']

LETTERS: List[str] = [
    chr(x) for x in range(ord('A'), ord('Z') + 1)
    if chr(x) not in ['I', 'O']
]

SPECIAL_CHARS: List[str] = ["警", "使", "领", "学", "挂", "港", "澳"]

# 不支持双层车牌的颜色
DOUBLE_UNSUPPORTED_COLORS: List[str] = [
    PlateColor.BLUE.value,
    PlateColor.GREEN_CAR.value,
    PlateColor.GREEN_TRUCK.value,
    PlateColor.BLACK.value,
    PlateColor.BLACK_SHI.value,
    PlateColor.WHITE.value,
    PlateColor.WHITE_ARMY.value
]

# 不支持双层的特殊字符
DOUBLE_UNSUPPORTED_CHARS: set = {"警", "使", "领", "港", "澳", "学"}
