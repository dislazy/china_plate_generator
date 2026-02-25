"""
车牌号码生成模块

提供中国车牌号码的随机生成功能，包括各种类型的车牌：
- 普通蓝牌、黄牌
- 新能源绿牌
- 白色警车/军车
- 黑色港澳/使领馆车牌
"""

from typing import List
import numpy as np

from plate_config import (
    PROVINCES, DIGITS, LETTERS, SPECIAL_CHARS,
    PLATE_LENGTH_NORMAL, PLATE_LENGTH_NEW_ENERGY
)


def random_select(data: List) -> any:
    """
    从列表中随机选择一个元素

    Args:
        data: 待选择的列表

    Returns:
        随机选择的元素
    """
    if not data:
        raise ValueError("Cannot select from empty list")
    return data[np.random.randint(len(data))]


def generate_plate_number_blue(length: int = PLATE_LENGTH_NORMAL) -> str:
    """
    生成普通蓝牌号码

    Args:
        length: 车牌长度，默认为7

    Returns:
        车牌号码字符串
    """
    if length not in [PLATE_LENGTH_NORMAL, PLATE_LENGTH_NEW_ENERGY]:
        raise ValueError(f"车牌长度必须是{PLATE_LENGTH_NORMAL}或{PLATE_LENGTH_NEW_ENERGY}")

    plate = random_select(PROVINCES)
    for _ in range(length - 1):
        plate += random_select(DIGITS + LETTERS)
    return plate


def generate_plate_number_yellow_gua() -> str:
    """
    生成黄色挂车车牌

    Returns:
        挂车车牌号码（6位字符+挂）
    """
    plate = generate_plate_number_blue()
    return plate[:6] + '挂'


def generate_plate_number_yellow_xue() -> str:
    """
    生成黄色教练车车牌

    Returns:
        教练车车牌号码（6位字符+学）
    """
    plate = generate_plate_number_blue()
    return plate[:6] + '学'


def generate_plate_number_white() -> str:
    """
    生成白色警车或军车车牌

    Returns:
        警车车牌（6位字符+警）或军车车牌（字母开头）
    """
    plate = generate_plate_number_blue()

    if np.random.random() > 0.5:
        return plate[:6] + '警'
    else:
        first_letter = random_select(LETTERS)
        return first_letter + plate[1:]


def generate_plate_number_black_gangao() -> str:
    """
    生成黑色港澳车牌

    Returns:
        港澳车牌号码（粤开头，6位字符，港澳结尾）
    """
    plate = generate_plate_number_blue()
    return '粤' + plate[1:6] + random_select(["港", "澳"])


def generate_plate_number_black_ling() -> str:
    """
    生成黑色领馆车牌

    Returns:
        领馆车牌号码（6位字符+领）
    """
    plate = generate_plate_number_blue()
    return plate[:6] + '领'


def generate_plate_number_black_shi() -> str:
    """
    生成黑色使领车牌

    Returns:
        使领车牌号码（使开头）
    """
    plate = generate_plate_number_blue()
    return '使' + plate[1:]


def calculate_board_bbox(polys: np.ndarray) -> List[int]:
    """
    计算边界框

    Args:
        polys: 多边形坐标数组

    Returns:
        边界框坐标 [x1, y1, x2, y2]
    """
    x1, y1 = np.min(polys, axis=0)
    x2, y2 = np.max(polys, axis=0)
    return [x1, y1, x2, y2]


if __name__ == '__main__':
    # 测试代码
    print("蓝牌:", generate_plate_number_blue())
    print("新能源:", generate_plate_number_blue(8))
    print("挂车:", generate_plate_number_yellow_gua())
    print("教练车:", generate_plate_number_yellow_xue())
    print("白牌:", generate_plate_number_white())
    print("港澳:", generate_plate_number_black_gangao())
    print("领馆:", generate_plate_number_black_ling())
    print("使领:", generate_plate_number_black_shi())