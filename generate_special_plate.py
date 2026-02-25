"""
生成指定车牌的主程序

允许用户生成指定号码、颜色、单双层的中国车牌图片

⚠️ 警告：
    本工具仅供学习、测试、研究使用，严禁用于任何非法用途！
    生成的车牌图片严禁用于任何真实的车辆上路行驶。
    伪造、变造车牌是严重违法行为，将承担法律责任。
"""

import argparse
import os
import cv2

from generate_multi_plate import MultiPlateGenerator, PlateColor


def parse_args() -> argparse.Namespace:
    """
    解析命令行参数

    Returns:
        参数命名空间
    """
    parser = argparse.ArgumentParser(
        description='中国车牌生成器 - 生成指定号码的车牌',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成新能源车牌
  python generate_special_plate.py --plate-number 粤A12345 --bg-color green_car

  # 生成双层黄色车牌
  python generate_special_plate.py --plate-number 湘999999 --double --bg-color yellow

  # 生成蓝色车牌（单层）
  python generate_special_plate.py --plate-number 粤A12345 --bg-color blue
        """
    )
    parser.add_argument(
        '--plate-number',
        default='云999999',
        help='车牌号码（7位或8位）'
    )
    parser.add_argument(
        '--bg-color',
        default='blue',
        help='车牌底板颜色: blue, yellow, green_car, green_truck, white, white_army, black, black_shi'
    )
    parser.add_argument(
        '--double',
        action='store_true',
        help='是否双层车牌（仅yellow支持）'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='输出目录（默认当前目录）'
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
    print(f"车牌号码: {args.plate_number}")
    print(f"底板颜色: {args.bg_color}")
    print(f"双层车牌: {'是' if args.double else '否'}")

    try:
        # 确保输出目录存在
        ensure_directory_exists(args.output_dir)

        # 初始化生成器
        generator = MultiPlateGenerator(args.plate_model_dir, args.font_dir)

        # 生成车牌
        print("正在生成车牌...")
        img = generator.generate_plate_special(
            args.plate_number,
            args.bg_color,
            args.double
        )

        # 保存图片
        filename = f"{args.plate_number}.jpg"
        filepath = os.path.join(args.output_dir, filename)
        cv2.imwrite(filepath, img)

        print(f"车牌已生成并保存到: {filepath}")

    except ValueError as e:
        print(f"错误: {e}")
        exit(1)
    except FileNotFoundError as e:
        print(f"错误: {e}")
        exit(1)
    except Exception as e:
        print(f"未知错误: {e}")
        exit(1)


if __name__ == '__main__':
    main()
