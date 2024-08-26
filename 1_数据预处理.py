import pandas as pd
import numpy as np

"""
选择python3.12版本
"""

# 定义一个函数来转换百分比字符串为数值
def convert_percentage(s):
    # 检查s是否为字符串，如果不是，则不进行转换
    if isinstance(s, str):
        # 尝试去除百分号并转换为浮点数
        try:
            # 先去除百分号，然后转换为浮点数，并除以100
            return float(s.replace('%', ''))
        except ValueError:
            # 如果转换失败，返回NaN
            return pd.NA
    else:
        # 如果s不是字符串，直接返回s
        return s


df = pd.read_excel('Table.xlsx', engine='openpyxl')
df['涨幅'] = df['涨幅'].apply(convert_percentage)
df['5日涨幅'] = df['5日涨幅'].apply(convert_percentage)
df['10日涨幅'] = df['10日涨幅'].apply(convert_percentage)

# 筛选涨幅大于1%且小于6%的数据
df = df[df['现价'] != '--']
df = df[(df['涨幅'] > 0.01) & (df['涨幅'] < 0.06)]
# 量比大于1
df['量比'] = df['量比'].astype(float)  # 转换为浮点数
df = df[df['量比'] > 1]
# 主力净量为正数
df = df[df['主力净量'] > 0]
# 5日涨幅为正数
df = df[df['5日涨幅'] > 0]
# 10日涨幅为正数
df = df[df['10日涨幅'] > 0]

# 删除TTM市盈率为空值的行
df = df.dropna(subset=['TTM市盈率'])

# 将筛选后的数据保存到新的Excel文件
df.to_excel('竞价交易策略.xlsx', index=False)