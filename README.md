# 中国车牌模拟生成器

## 介绍
中国车牌模拟生成器 - 支持生成各种类型的中国车牌图片

## 致谢

本项目借鉴了以下项目并进行优化改进：

- **原始项目**: [Pengfei8324/chinese_license_plate_generator](https://github.com/Pengfei8324/chinese_license_plate_generator)

### 主要改进内容

基于原项目，本项目进行了以下优化和改进：

1. **代码重构**
   - 模块化设计，分离配置、生成逻辑
   - 添加类型提示（Type Hints）
   - 完善文档字符串
   - 遵循 PEP 8 代码规范

2. **功能增强**
   - 添加参数验证和错误提示
   - 支持 Poetry 包管理
   - 改进命令行参数处理
   - 提供更友好的配置方式（main.py）

3. **用户体验**
   - 简化使用流程，只需修改配置即可运行
   - 改进错误提示信息
   - 添加使用示例和文档

感谢原作者的分享！

---

## 许可证

本项目采用 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件

基于 [Pengfei8324/chinese_license_plate_generator](https://github.com/Pengfei8324/chinese_license_plate_generator) 项目优化改进

## 支持车牌
- 黄色、白色、黑色、新能源车牌
- 单层、双层车牌
- 警车、军车、教练车、挂车、港澳车牌、使领馆车牌

---

## ⚠️ 重要声明与免责条款

### 使用警告

**本工具仅供学习、测试、研究使用，严禁用于任何非法用途！**

### 使用限制

1. **禁止上路**
   - 生成的车牌图片**严禁**用于任何真实的车辆
   - 禁止制作、使用伪造车牌进行上路行驶
   - 伪造、变造车牌是**严重违法行为**

2. **遵守法律法规**
   - 本项目生成的车牌为**模拟图片**，不构成真实车牌
   - 使用者必须遵守《中华人民共和国道路交通安全法》等相关法律法规
   - 禁止用于诈骗、冒充、欺诈等违法活动

3. **合法用途**
   - ✅ 学习计算机视觉和图像处理
   - ✅ 测试车牌识别算法
   - ✅ 学术研究和教学演示
   - ✅ 开发车牌识别系统

4. **禁止用途**
   - ❌ 伪造真实车牌
   - ❌ 用于任何车辆上牌或上路
   - ❌ 用于违法犯罪活动
   - ❌ 用于商业欺诈或冒充

### 免责声明

1. 本项目仅为**学习研究工具**，所生成的车牌图片仅用于测试、学习、研究等合法目的。

2. 项目维护者**不对**因误用本项目而产生的任何法律后果承担责任。

3. 使用者应自行承担使用本项目的所有法律责任，确保遵守当地法律法规。

4. 本项目生成的车牌**不具有**任何法律效力，不能替代真实车牌。

5. 如发现本项目被用于非法用途，项目维护者保留追究法律责任的权利。

### 法律提示

根据《中华人民共和国刑法》第二百八十条：
- **伪造、变造、买卖或者盗窃、抢夺、毁灭国家机关的公文、证件、印章的**，处三年以下有期徒刑、拘役、管制或者剥夺政治权利；情节严重的，处三年以上十年以下有期徒刑。
- **伪造、变造、买卖居民身份证、护照、社会保障卡、驾驶证等依法可以用于证明身份的证件的**，处三年以下有期徒刑、拘役、管制或者剥夺政治权利；情节严重的，处三年以上七年以下有期徒刑。

**请勿以身试法！**

---

## 快速开始

### 1. 安装依赖

**使用 pip：**
```bash
pip3 install -r requirements.txt
```

**使用 Poetry（推荐）：**
```bash
poetry install
```

### 2. 使用方式

#### ⭐ 方式一：简单配置（推荐）

打开 `main.py` 文件，在 `main()` 函数中配置参数：

```python
def main():
    # 方式1: 生成指定车牌
    generate_single = True

    plate_number = "粤A12345"   # 车牌号码
    bg_color = "green_car"        # 底板颜色
    is_double = False             # 是否双层
    output_path = "车牌.jpg"      # 保存路径
```

**三种生成模式：**

1. **生成指定车牌** - 单张车牌生成
```python
generate_single = True
plate_number = "粤A12345"
bg_color = "green_car"
is_double = False
output_path = "车牌.jpg"
```

2. **随机生成多张** - 批量随机生成
```python
generate_multiple = True
number_of_plates = 10      # 生成数量
save_directory = "output"  # 保存目录
```

3. **批量生成指定车牌** - 多个指定车牌
```python
generate_batch = True
plates_config = [
    ("车牌号", "颜色", 是否双层, "文件名"),
    ("粤A12345", "green_car", False, "新能源.jpg"),
    ("粤B23456", "blue", False, "蓝牌.jpg"),
]
```

**运行：**
```bash
poetry run python main.py
```

---

#### 方式二：命令行参数

**生成指定车牌：**
```bash
poetry run python generate_special_plate.py --plate-number 粤A12345 --bg-color green_car
```

**生成双层车牌：**
```bash
poetry run python generate_special_plate.py --plate-number 湘999999 --double --bg-color yellow
```

**随机生成多张：**
```bash
poetry run python generate_multi_plate.py --number 10 --save-adr output
```

---

## 参数说明

### 车牌颜色 (bg_color)

| 颜色代码 | 说明 | 是否支持双层 |
|---------|------|------------|
| `blue` | 普通蓝牌 | 否 |
| `yellow` | 黄色中型车 | 是 |
| `green_car` | 新能源轿车 | 否 |
| `green_truck` | 新能源卡车 | 否 |
| `white` | 白色警车 | 否 |
| `white_army` | 白色军车 | 否 |
| `black` | 粤港澳 | 否 |
| `black_shi` | 使领馆 | 否 |

### 车牌号码规则

- **普通车牌（7位）**：省份代码 + 6位字符（字母/数字）
- **新能源车牌（8位）**：省份代码 + 7位字符
- **特殊字符**：警、使、领、学、挂、港、澳

**注意：**
- 新能源车牌必须是8位
- 字母 I 和 O 不在车牌中使用
- 首字符必须是省份代码或字母（军车）

### 双层车牌规则

- **仅黄色车牌**支持双层
- **挂车**必须使用双层
- **警车、使领馆、港澳、学警、新能源**必须是单层

---

## 配置示例

### 示例1：生成新能源车牌
```python
generate_single = True
plate_number = "粤A12345"
bg_color = "green_car"
is_double = False
```

### 示例2：生成双层黄牌
```python
generate_single = True
plate_number = "湘999999"
bg_color = "yellow"
is_double = True
```

### 示例3：随机生成100张车牌
```python
generate_multiple = True
number_of_plates = 100
save_directory = "plates"
```

### 示例4：批量生成多种车牌
```python
generate_batch = True
plates_config = [
    ("粤A12345", "green_car", False, "新能源轿车.jpg"),
    ("渝B234567", "green_truck", False, "新能源卡车.jpg"),
    ("湘999999", "yellow", True, "双层黄牌.jpg"),
    ("粤C34567", "blue", False, "蓝牌.jpg"),
    ("京D45678", "white", False, "警车.jpg"),
]
```

---

## 文件说明

- `main.py` - 主程序，修改参数后运行
- `generate_special_plate.py` - 生成指定车牌脚本
- `generate_multi_plate.py` - 随机生成车牌脚本
- `plate_number.py` - 车牌号码生成模块
- `plate_config.py` - 配置常量模块
- `plate_model/` - 车牌底板图片目录
- `font_model/` - 字符图片目录

---

## 常见问题

**Q: 为什么报错 "底板图片不存在"？**
A: 确保 plate_model/ 目录下有对应颜色的底板图片。

**Q: 为什么不能生成双层蓝牌？**
A: 只有黄色车牌支持双层，其他颜色仅支持单层。

**Q: 新能源车牌可以是7位吗？**
A: 新能源车牌必须是8位，7位为普通车牌。

---

## ⚖️ 最终免责声明

**最后警告：本项目生成的车牌图片仅供学习、测试、研究使用！**

**严禁：**
- 将生成的车牌用于真实车辆
- 伪造、变造车牌
- 任何违法用途

**后果自负：**
- 使用本工具的任何法律风险由使用者自行承担
- 如被用于非法用途，后果严重，追究法律责任

**请珍惜自由，遵纪守法！**

---

## 相关链接

- **原始项目**: [Pengfei8324/chinese_license_plate_generator](https://github.com/Pengfei8324/chinese_license_plate_generator)
- **项目说明**: [知乎文章](https://zhuanlan.zhihu.com/p/101352235)
- **Windows字符问题**: [Gitee Issue](https://gitee.com/leijd/chinese_license_plate_generator/issues/I1NOC7)
