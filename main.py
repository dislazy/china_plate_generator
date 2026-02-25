"""
车牌生成器主程序

提供简单的API调用方式，直接在代码中配置参数即可使用

⚠️ 警告：
    本工具仅供学习、测试、研究使用，严禁用于任何非法用途！
    生成的车牌图片严禁用于任何真实的车辆上路行驶。
    伪造、变造车牌是严重违法行为，将承担法律责任。
"""

from generate_multi_plate import MultiPlateGenerator


def main():
    """
    主函数 - 在这里配置你的参数并执行

    使用示例：
    1. 生成指定车牌
    2. 随机生成多张车牌
    3. 指定保存路径
    """

    # ==================== 配置区域 ====================

    # 方式1: 生成指定车牌
    generate_single = True  # 是否生成指定车牌

    if generate_single:
        # 指定车牌配置
        plate_number = "粤A12345"  # 车牌号码（7位或8位）
        bg_color = "green_car"  # 底板颜色: blue, yellow, green_car, green_truck, white, white_army, black, black_shi
        is_double = False  # 是否双层车牌（仅yellow支持）
        output_path = f"{plate_number}.jpg"  # 保存路径

        # 生成指定车牌
        generator = MultiPlateGenerator()
        img = generator.generate_plate_special(plate_number, bg_color, is_double)
        import cv2
        cv2.imwrite(output_path, img)
        print(f"车牌已生成: {plate_number}")
        print(f"保存路径: {output_path}")
        return

    # 方式2: 随机生成多张车牌
    generate_multiple = False  # 是否随机生成多张车牌

    if generate_multiple:
        import os
        from tqdm import tqdm

        number_of_plates = 5  # 生成数量
        save_directory = "output"  # 保存目录

        # 确保输出目录存在
        os.makedirs(save_directory, exist_ok=True)

        # 生成车牌
        generator = MultiPlateGenerator()
        print(f"正在生成 {number_of_plates} 张车牌...")

        for i in tqdm(range(number_of_plates)):
            try:
                img, _, gt_plate_number, bg_color, is_double = generator.generate_plate()
                filename = f'{gt_plate_number}_{bg_color}_{is_double}.jpg'
                filepath = os.path.join(save_directory, filename)
                cv2.imwrite(filepath, img)
                print(f"  {i+1}. {filename}")
            except Exception as e:
                print(f"  生成失败: {e}")

        print(f"\n完成！车牌已保存到: {save_directory}")
        return

    # 方式3: 生成多张指定车牌
    generate_batch = True  # 是否批量生成指定车牌

    if generate_batch:
        import os
        import cv2

        # 批量配置
        plates_config = [
            # (车牌号码, 底板颜色, 是否双层, 文件名)
            ("粤A12345", "green_car", False, "新能源轿车.jpg"),
            ("渝B234567", "green_truck", False, "新能源卡车.jpg"),
            ("湘999999", "yellow", True, "双层黄牌.jpg"),
            ("粤C34567", "blue", False, "蓝牌.jpg"),
            ("京D45678", "white", False, "警车.jpg"),
        ]

        save_directory = "batch_output"  # 保存目录

        # 确保输出目录存在
        os.makedirs(save_directory, exist_ok=True)

        # 批量生成
        generator = MultiPlateGenerator()
        print(f"正在批量生成 {len(plates_config)} 张车牌...")

        for i, (plate_number, bg_color, is_double, filename) in enumerate(plates_config):
            try:
                output_path = os.path.join(save_directory, filename)
                img = generator.generate_plate_special(plate_number, bg_color, is_double)
                cv2.imwrite(output_path, img)
                print(f"  {i+1}. {filename} ({plate_number})")
            except Exception as e:
                print(f"  生成失败 {plate_number}: {e}")

        print(f"\n完成！车牌已保存到: {save_directory}")
        return

    print("请在main函数中配置你的参数（设置 generate_single, generate_multiple, generate_batch 为 True）")


if __name__ == '__main__':
    main()
