"""
中国车牌生成模块

提供随机生成和指定生成中国车牌的功能，支持多种类型：
- 蓝色普通车牌
- 黄色中型车/挂车/教练车
- 白色警车/军车
- 黑色港澳/使领馆车牌
- 新能源绿牌（轿车/卡车）

⚠️ 警告：
    本工具仅供学习、测试、研究使用，严禁用于任何非法用途！
    生成的车牌图片严禁用于任何真实的车辆上路行驶。
    伪造、变造车牌是严重违法行为，将承担法律责任。
"""

from typing import List, Tuple, Dict, Optional
from enum import Enum
import os
import argparse
from glob import glob
import numpy as np
import cv2
from tqdm import tqdm

from plate_number import (
    random_select, generate_plate_number_white, generate_plate_number_yellow_xue,
    generate_plate_number_black_gangao, generate_plate_number_black_shi,
    generate_plate_number_black_ling, generate_plate_number_blue,
    generate_plate_number_yellow_gua, LETTERS, DIGITS,
    PLATE_LENGTH_NORMAL, PLATE_LENGTH_NEW_ENERGY, PROVINCES
)


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


# 车牌尺寸常量
HEIGHT_SINGLE = 140
HEIGHT_DOUBLE = 220
WIDTH_7_CHARS = 440
WIDTH_8_CHARS = 480

# 字符位置配置
FONT_WIDTH_NORMAL = 45
FONT_WIDTH_NEW_ENERGY = 43
FONT_WIDTH_DOUBLE = 65
STEP_SPLIT_7 = 34
STEP_SPLIT_8 = 49
STEP_FONT_7 = 12
STEP_FONT_8 = 9
STEP_FONT_DOUBLE = 15

# 不支持双层车牌的颜色
DOUBLE_UNSUPPORTED_COLORS = [
    PlateColor.BLUE.value,
    PlateColor.GREEN_CAR.value,
    PlateColor.GREEN_TRUCK.value,
    PlateColor.BLACK.value,
    PlateColor.BLACK_SHI.value,
    PlateColor.WHITE.value,
    PlateColor.WHITE_ARMY.value
]

# 不支持双层的特殊字符
DOUBLE_UNSUPPORTED_CHARS = {"警", "使", "领", "港", "澳", "学"}


def get_location_data(length: int = PLATE_LENGTH_NORMAL,
                      split_id: int = 1,
                      height: int = HEIGHT_SINGLE) -> np.ndarray:
    """
    获取车牌号码在底牌中的位置

    Args:
        length: 车牌字符数，7为普通车牌，8为新能源车牌
        split_id: 分割空隙位置（1, 2, 4）
        height: 车牌高度，140为单层，220为双层

    Returns:
        字符位置数组，每行为 [x1, y1, x2, y2]
    """
    if length not in [PLATE_LENGTH_NORMAL, PLATE_LENGTH_NEW_ENERGY]:
        raise ValueError(f"车牌长度必须是{PLATE_LENGTH_NORMAL}或{PLATE_LENGTH_NEW_ENERGY}")

    if height not in [HEIGHT_SINGLE, HEIGHT_DOUBLE]:
        raise ValueError(f"车牌高度必须是{HEIGHT_SINGLE}或{HEIGHT_DOUBLE}")

    location_xy = np.zeros((length, 4), dtype=np.int32)

    if height == HEIGHT_SINGLE:
        # 单层车牌，y轴坐标固定
        location_xy[:, 1] = 25
        location_xy[:, 3] = 115

        step_split = STEP_SPLIT_7 if length == PLATE_LENGTH_NORMAL else STEP_SPLIT_8
        step_font = STEP_FONT_7 if length == PLATE_LENGTH_NORMAL else STEP_FONT_8
        width_font = FONT_WIDTH_NORMAL

        for i in range(length):
            if i == 0:
                location_xy[i, 0] = 15
            elif i == split_id:
                location_xy[i, 0] = location_xy[i - 1, 2] + step_split
            else:
                location_xy[i, 0] = location_xy[i - 1, 2] + step_font

            if length == PLATE_LENGTH_NEW_ENERGY and i > 0:
                width_font = FONT_WIDTH_NEW_ENERGY
            location_xy[i, 2] = location_xy[i, 0] + width_font
    else:
        # 双层车牌
        location_xy[0, :] = [110, 15, 190, 75]
        location_xy[1, :] = [250, 15, 330, 75]

        for i in range(2, length):
            location_xy[i, 1] = 90
            location_xy[i, 3] = 200
            if i == 2:
                location_xy[i, 0] = 27
            else:
                location_xy[i, 0] = location_xy[i - 1, 2] + STEP_FONT_DOUBLE
            location_xy[i, 2] = location_xy[i, 0] + FONT_WIDTH_DOUBLE

    return location_xy


def copy_font_to_plate(img: np.ndarray,
                       font_img: np.ndarray,
                       bbox: List[int],
                       bg_color: str,
                       is_red: bool) -> np.ndarray:
    """
    将字符贴到车牌底板上

    Args:
        img: 车牌底板图像
        font_img: 字符图像
        bbox: 字符位置 [x1, y1, x2, y2]
        bg_color: 背景颜色
        is_red: 是否为红色字符

    Returns:
        贴完字符后的车牌图像
    """
    x1, y1, x2, y2 = bbox
    font_img_resized = cv2.resize(font_img, (x2 - x1, y2 - y1))
    img_crop = img[y1:y2, x1:x2, :]

    if is_red:
        img_crop[font_img_resized < 200, :] = [0, 0, 255]
    elif 'blue' in bg_color or 'black' in bg_color:
        img_crop[font_img_resized < 200, :] = [255, 255, 255]
    else:
        img_crop[font_img_resized < 200, :] = [0, 0, 0]

    return img


class MultiPlateGenerator:
    """中国车牌生成器类"""

    def __init__(self, plate_model_dir: str = 'plate_model', font_dir: str = 'font_model'):
        """
        初始化车牌生成器

        Args:
            plate_model_dir: 车牌底板图片目录
            font_dir: 字符图片目录
        """
        self.plate_model_dir = plate_model_dir
        self.font_dir = font_dir

        # 验证目录是否存在
        if not os.path.exists(plate_model_dir):
            raise FileNotFoundError(f"车牌底板目录不存在: {plate_model_dir}")
        if not os.path.exists(font_dir):
            raise FileNotFoundError(f"字符图片目录不存在: {font_dir}")

        # 加载字符图片
        self.font_imgs: Dict[str, np.ndarray] = self._load_font_images()

        # 预计算字符位置
        self.location_xys: Dict[str, np.ndarray] = self._precompute_locations()

    def _load_font_images(self) -> Dict[str, np.ndarray]:
        """
        加载并预处理所有字符图片

        Returns:
            字符图片字典，key为字符名称，value为图像数组
        """
        font_imgs = {}
        font_filenames = glob(os.path.join(self.font_dir, '*.jpg'))

        for font_filename in font_filenames:
            try:
                font_img = cv2.imdecode(np.fromfile(font_filename, dtype=np.uint8), 0)

                if '140' in font_filename:
                    font_img = cv2.resize(font_img, (FONT_WIDTH_NORMAL, 90))
                elif '220' in font_filename:
                    font_img = cv2.resize(font_img, (FONT_WIDTH_DOUBLE, 110))
                elif font_filename.split('_')[-1].split('.')[0] in LETTERS + DIGITS:
                    font_img = cv2.resize(font_img, (FONT_WIDTH_NEW_ENERGY, 90))

                font_key = os.path.basename(font_filename).split('.')[0]
                font_imgs[font_key] = font_img
            except Exception as e:
                print(f"警告: 无法加载字符图片 {font_filename}: {e}")

        return font_imgs

    def _precompute_locations(self) -> Dict[str, np.ndarray]:
        """
        预计算所有可能的字符位置

        Returns:
            位置字典，key为"length_split_height"，value为位置数组
        """
        location_xys = {}
        for length in [PLATE_LENGTH_NORMAL, PLATE_LENGTH_NEW_ENERGY]:
            for split_id in [1, 2, 4]:
                for height in [HEIGHT_SINGLE, HEIGHT_DOUBLE]:
                    key = f"{length}_{split_id}_{height}"
                    location_xys[key] = get_location_data(length=length, split_id=split_id, height=height)
        return location_xys

    def _get_split_id(self, plate_number: str) -> int:
        """
        根据车牌号码确定分割位置

        Args:
            plate_number: 车牌号码

        Returns:
            分割位置（1, 2, 4）
        """
        if '警' in plate_number:
            return 1
        elif '使' in plate_number:
            return 4
        return 2

    def _get_location_multi(self, plate_number: str, height: int = HEIGHT_SINGLE) -> np.ndarray:
        """
        获取字符位置数组

        Args:
            plate_number: 车牌号码
            height: 车牌高度

        Returns:
            字符位置数组
        """
        length = len(plate_number)
        split_id = self._get_split_id(plate_number)
        key = f"{length}_{split_id}_{height}"

        if key not in self.location_xys:
            raise ValueError(f"未找到位置配置: {key}")

        return self.location_xys[key]

    def generate_plate_number(self) -> Tuple[str, str, bool]:
        """
        随机生成车牌号码、底板颜色和单双层标志

        Returns:
            (车牌号码, 底板颜色, 是否双层)
        """
        rate = np.random.random()

        # 60% 生成蓝牌或新能源
        if rate > 0.4:
            plate_number = generate_plate_number_blue(
                length=random_select([PLATE_LENGTH_NORMAL, PLATE_LENGTH_NEW_ENERGY])
            )
        else:
            # 40% 生成其他类型
            funcs = [
                generate_plate_number_white,
                generate_plate_number_yellow_xue,
                generate_plate_number_yellow_gua,
                generate_plate_number_black_gangao,
                generate_plate_number_black_shi,
                generate_plate_number_black_ling
            ]
            plate_number = random_select(funcs)()

        # 确定底板颜色
        bg_color = self._determine_bg_color(plate_number)

        # 确定是否双层
        is_double = self._determine_is_double(plate_number, bg_color)

        return plate_number, bg_color, is_double

    def _determine_bg_color(self, plate_number: str) -> str:
        """
        根据车牌号码确定底板颜色

        Args:
            plate_number: 车牌号码

        Returns:
            底板颜色
        """
        plate_set = set(plate_number)

        if len(plate_number) == PLATE_LENGTH_NEW_ENERGY:
            return random_select(['green_car'] * 10 + ['green_truck'])
        elif plate_set & {'使', '领', '港', '澳'}:
            return 'black' if '使' not in plate_number else 'black_shi'
        elif '警' in plate_number or plate_number[0] in LETTERS:
            return 'white'
        elif plate_set & {'学', '挂'}:
            return 'yellow'

        return random_select(['blue', 'yellow'])

    def _determine_is_double(self, plate_number: str, bg_color: str) -> bool:
        """
        确定是否为双层车牌

        Args:
            plate_number: 车牌号码
            bg_color: 底板颜色

        Returns:
            是否为双层车牌
        """
        # 挂车必须是双层
        if '挂' in plate_number:
            return True

        # 特殊字符车牌、新能源、蓝牌必须是单层
        special_chars = {'使', '领', '港', '澳', '学', '警'}
        if (set(plate_number) & special_chars) or len(plate_number) == PLATE_LENGTH_NEW_ENERGY or bg_color == 'blue':
            return False

        # 黄牌随机选择，倾向双层
        return random_select([False] + [True] * 3)

    def _get_font_image(self, char: str, height: int, index: int, is_new_energy: bool) -> Optional[np.ndarray]:
        """
        获取字符图片

        Args:
            char: 字符
            height: 车牌高度
            index: 字符索引
            is_new_energy: 是否为新能源车牌

        Returns:
            字符图像数组
        """
        if is_new_energy:
            key = f"green_{char}"
        elif f"{height}_{char}" in self.font_imgs:
            key = f"{height}_{char}"
        else:
            key = f"220_up_{char}" if index < 2 else f"220_down_{char}"

        return self.font_imgs.get(key)

    def _is_red_char(self, char: str, index: int, plate_number: str) -> bool:
        """
        判断字符是否为红色

        Args:
            char: 当前字符
            index: 字符索引
            plate_number: 车牌号码

        Returns:
            是否为红色字符
        """
        if (index == 0 and plate_number[0] in LETTERS) or char in ['警', '使', '领']:
            return True
        if index == 1 and plate_number[0] in LETTERS and np.random.random() > 0.5:
            return True
        return False

    def _apply_enhancement(self, font_img: np.ndarray) -> np.ndarray:
        """
        应用图像增强效果

        Args:
            font_img: 字符图像

        Returns:
            增强后的图像
        """
        k = np.random.randint(1, 6)
        kernel = np.ones((k, k), np.uint8)

        if np.random.random() > 0.5:
            return np.copy(cv2.erode(font_img, kernel, iterations=1))
        else:
            return np.copy(cv2.dilate(font_img, kernel, iterations=1))

    def generate_plate(self, enhance: bool = False) -> Tuple[np.ndarray, np.ndarray, str, str, bool]:
        """
        随机生成车牌图片

        Args:
            enhance: 是否应用图像增强

        Returns:
            (车牌图像, 位置数组, 车牌号码, 底板颜色, 是否双层)
        """
        plate_number, bg_color, is_double = self.generate_plate_number()
        return self._generate_plate_image(plate_number, bg_color, is_double, enhance)

    def _generate_plate_image(self,
                               plate_number: str,
                               bg_color: str,
                               is_double: bool,
                               enhance: bool) -> Tuple[np.ndarray, np.ndarray, str, str, bool]:
        """
        生成车牌图片的内部实现

        Args:
            plate_number: 车牌号码
            bg_color: 底板颜色
            is_double: 是否双层
            enhance: 是否应用图像增强

        Returns:
            (车牌图像, 位置数组, 车牌号码, 底板颜色, 是否双层)
        """
        height = HEIGHT_DOUBLE if is_double else HEIGHT_SINGLE
        is_new_energy = len(plate_number) == PLATE_LENGTH_NEW_ENERGY

        # 获取底板图片
        number_xy = self._get_location_multi(plate_number, height)
        img_plate_model = self._load_plate_model(bg_color, height, is_new_energy)

        # 渲染字符
        for i, char in enumerate(plate_number):
            font_img = self._get_font_image(char, height, i, is_new_energy)
            if font_img is None:
                print(f"警告: 未找到字符图片 {char}")
                continue

            is_red = self._is_red_char(char, i, plate_number)

            if enhance:
                font_img = self._apply_enhancement(font_img)

            img_plate_model = copy_font_to_plate(
                img_plate_model, font_img,
                number_xy[i, :], bg_color, is_red
            )

        # 应用模糊效果
        img_plate_model = cv2.blur(img_plate_model, (3, 3))

        return img_plate_model, number_xy, plate_number, bg_color, is_double

    def _load_plate_model(self, bg_color: str, height: int, is_new_energy: bool) -> np.ndarray:
        """
        加载车牌底板图片

        Args:
            bg_color: 底板颜色
            height: 车牌高度
            is_new_energy: 是否为新能源车牌

        Returns:
            底板图像
        """
        img_path = os.path.join(self.plate_model_dir, f'{bg_color}_{height}.PNG')

        if not os.path.exists(img_path):
            raise FileNotFoundError(f"底板图片不存在: {img_path}")

        img_plate_model = cv2.imread(img_path)
        if img_plate_model is None:
            raise ValueError(f"无法加载底板图片: {img_path}")

        width = WIDTH_8_CHARS if is_new_energy else WIDTH_7_CHARS
        return cv2.resize(img_plate_model, (width, height))

    def generate_plate_special(self,
                               plate_number: str,
                               bg_color: str,
                               is_double: bool,
                               enhance: bool = False) -> np.ndarray:
        """
        生成指定号码、颜色的车牌图片

        Args:
            plate_number: 车牌号码
            bg_color: 背景颜色，可选值见PlateColor枚举
            is_double: 是否双层
            enhance: 是否应用图像增强

        Returns:
            车牌图像

        Raises:
            ValueError: 参数组合无效时抛出异常
        """
        # 验证车牌号码
        self._validate_plate_number(plate_number)

        # 验证底板颜色
        self._validate_bg_color(bg_color)

        # 验证双层车牌的合法性
        if is_double:
            self._validate_double_plate(plate_number, bg_color)

        return self._generate_plate_image(plate_number, bg_color, is_double, enhance)[0]

    def _validate_plate_number(self, plate_number: str) -> None:
        """
        验证车牌号码格式

        Args:
            plate_number: 车牌号码

        Raises:
            ValueError: 车牌号码格式无效
        """
        if not plate_number:
            raise ValueError("车牌号码不能为空")

        if len(plate_number) not in [PLATE_LENGTH_NORMAL, PLATE_LENGTH_NEW_ENERGY]:
            raise ValueError(f"车牌号码长度必须是{PLATE_LENGTH_NORMAL}或{PLATE_LENGTH_NEW_ENERGY}位")

        if plate_number[0] not in PROVINCES and plate_number[0] not in LETTERS:
            raise ValueError("车牌号码首位必须是省份代码或字母")

        # 验证剩余字符
        for char in plate_number[1:]:
            if char not in LETTERS and char not in DIGITS and char not in SPECIAL_CHARS:
                raise ValueError(f"车牌号码包含无效字符: {char}")

    def _validate_bg_color(self, bg_color: str) -> None:
        """
        验证底板颜色是否有效

        Args:
            bg_color: 底板颜色

        Raises:
            ValueError: 底板颜色无效
        """
        valid_colors = [color.value for color in PlateColor]
        if bg_color not in valid_colors:
            raise ValueError(f"底板颜色必须是以下之一: {', '.join(valid_colors)}")

    def _validate_double_plate(self, plate_number: str, bg_color: str) -> None:
        """
        验证双层车牌参数

        Args:
            plate_number: 车牌号码
            bg_color: 底板颜色

        Raises:
            ValueError: 双层车牌参数无效
        """
        if bg_color in DOUBLE_UNSUPPORTED_COLORS:
            raise ValueError(f'{bg_color} 车牌不支持双层（只能使用单层）')

        if any(char in plate_number for char in DOUBLE_UNSUPPORTED_CHARS):
            raise ValueError(f'包含特殊字符的车牌（使领港澳学警）不支持双层（只能使用单层）')

        if len(plate_number) == PLATE_LENGTH_NEW_ENERGY:
            raise ValueError(f'新能源车牌（{PLATE_LENGTH_NEW_ENERGY}位）不支持双层（只能使用单层）')


def parse_args() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        参数命名空间
    """
    parser = argparse.ArgumentParser(
        description='中国车牌生成器 - 随机生成各种类型的中国车牌'
    )
    parser.add_argument(
        '--number',
        default=10,
        type=int,
        help='生成车牌数量'
    )
    parser.add_argument(
        '--save-adr',
        default='multi_val',
        help='车牌保存路径'
    )
    parser.add_argument(
        '--plate-model-dir',
        default='plate_model',
        help='车牌底板图片目录'
    )
    parser.add_argument(
        '--font-dir',
        default='font_model',
        help='字符图片目录'
    )
    return parser.parse_args()


def ensure_directory_exists(path: str) -> None:
    """
    确保目录存在，不存在则创建

    Args:
        path: 目录路径
    """
    os.makedirs(path, exist_ok=True)


def main() -> None:
    """主函数"""
    args = parse_args()
    print(f"参数: {args}")
    print(f"保存路径: {args.save_adr}")

    # 确保输出目录存在
    ensure_directory_exists(args.save_adr)

    # 初始化生成器
    generator = MultiPlateGenerator(args.plate_model_dir, args.font_dir)

    # 生成车牌
    print(f"正在生成 {args.number} 张车牌...")
    for _ in tqdm(range(args.number)):
        try:
            img, _, gt_plate_number, bg_color, is_double = generator.generate_plate()
            filename = f'{gt_plate_number}_{bg_color}_{is_double}.jpg'
            filepath = os.path.join(args.save_adr, filename)
            cv2.imwrite(filepath, img)
        except Exception as e:
            print(f"警告: 生成车牌失败: {e}")

    print(f"完成！车牌已保存到: {args.save_adr}")


if __name__ == '__main__':
    main()