# China-University-Obituary-Analyze

## 项目简介
为中国高校的讣告数据提供标准化的简易分析与绘图代码，这可以使大家不必费力写一些基础的数据可视化相关代码。

## 数据格式
标准化数据文件须为.csv格式，数据表中分四列，分别为：Name, Time, Age, Place；分别表示：姓名、去世日期、去世时年龄、去世地点。

具体可参考我们给出的示例数据文件[university_1.csv](university_1.csv)，该示例数据来自真实的中国华北地区某所高校2019至2022年全部的公开发布的讣告信息，出于尊重与隐私保护的考虑，示例数据仅展示去世日期(Time)与年龄(Age)，而略去姓名(Name)与去世地点(Place)。

使用本仓库的数据绘图代码时，须参照上述格式自行采集相关数据，并确保自己的数据文件格式与我们给出的示例数据文件[university_1.csv](university_1.csv)的格式相同，否则代码会报错。

去世日期(Time)格式如: 2022/12/31，表示2022年12月31日。

年龄(Age)格式为大于0的正整数。

## 使用方法
### 1. 初始化数据
```python
from analyze import Analyzer

analyzer = Analyzer(csv_file_path='university_1.csv', language='zh-hans')
```

**csv_file_path**: 你的讣告数据csv文件的路径

**language**: 语言设定，默认为简体中文'zh-hans'，目前可选语言还有英文'en'。语言会影响最终绘制的图像中的文字的语言，如图像标题、坐标轴文字等。

语言翻译内容在[language_translation.py](language_translation.py)中。

### 2. 绘制不同年份下每个月份讣告数量对比图
```python
analyzer.plot_obituary_number_data_group_by_month(year_list=['2019', '2020', '2021', '2022'])
```
**year_list**: 指定讣告数据文件涵盖的年份，这必须与你自己的数据相匹配。

根据示例数据文件[university_1.csv](university_1.csv)得到的结果图绘制如下：
![](group_by_month_zhhans.png?raw=true "某高校不同年份下每月讣告数量图")

### 3. 绘制不同年份下按月累加的讣告数量对比图
```python
analyzer.plot_cumulative_obituary_number_by_month(year_list=['2019', '2020', '2021', '2022'])
```
**year_list**: 指定讣告数据文件涵盖的年份，这必须与你自己的数据相匹配。

根据示例数据文件[university_1.csv](university_1.csv)得到的结果图绘制如下：
![](cum_by_month_zhhans.png?raw=true "某高校不同年份下每月讣告数量图")

## 建议与贡献
欢迎在Issues中提出任何反馈与建议，比如你希望对讣告数据进行哪些分析与可视化，我们会尽力与尽快实现。


## 免责声明
本仓库全部内容旨在学习与探究Python数据分析与数据可视化内容，仅供学习与教育使用。不包含任何涉密与敏感信息。全部代码均为数据分析、数据可视化相关的开源代码，不包含任何恶意程序与恶意代码。不提供任何数据采集相关的代码与工具。对使用本项目造成的任何后果不承担责任。
