"""
本策略为简单移动平均策略，当5日均线上传10日均线时，第二天买入股票
"""

import matplotlib.pyplot as plt
# import seaborn
# plt.style.use('seaborn')             ggplot;
import matplotlib as mpl
mpl.rcParams['font.family'] = 'serif'               #解决一些字体显示乱码问题
import warnings; warnings.simplefilter('ignore')       #忽略警告信息；

import numpy as np
import pandas as pd
import yfinance as yf

import matplotlib.dates as mdates
from matplotlib.patches import FancyArrowPatch


# 计算股票指标
def plot_stock_strategy(ticker, start_date, end_date, short, long, frequency):
    # 获取股票数据
    data = yf.Ticker(ticker).history(period="max", interval=frequency,
                                     start=start_date, end=end_date, prepost=False,
                                     actions=False, auto_adjust=False,
                                     back_adjust=False, proxy=None,
                                     rounding=False, many=True)
    data.dropna(inplace=True)  # 删除包含NaN的行

    # 计算5日和10日简单移动平均线
    data['SMA_short'] = data['Close'].rolling(short).mean()
    data['SMA_long'] = data['Close'].rolling(long).mean()
    # 计算股票收益率
    data['returns'] = np.log(data['Close'] / data['Close'].shift(1))
    data['returns_dis'] = data['Close'] / data['Close'].shift(1) - 1
    # 根据5日均线和10日均线确定持仓位置
    data['position'] = np.where(data['SMA_short'] > data['SMA_long'], 1, 0)
    # 去除NaN值
    data.dropna(inplace=True)
    # 计算策略收益
    data['strategy'] = data['position'].shift(1) * data['returns']
    # 计算累计收益
    sum_returns = data['returns'].cumsum().apply(np.exp)
    sum_strategy = data['strategy'].cumsum().apply(np.exp)
    # 打印累计收益
    print(f"Sum of 'returns': {sum_returns}")
    print(f"Sum of 'strategy': {sum_strategy}")
    return data

# 计算胜率
def calculate_win_rate(data):
    data['signal'] = np.where((data['strategy'] > 0) & (data['position'].shift(1) == 1), 1, 0)
    data['signal'] = np.where((data['strategy'] < 0) & (data['position'].shift(1) == 1), -1, data['signal'])
    win_count = (data['signal'] == 1).sum()
    loss_count = (data['signal'] == -1).sum()
    print(f'win_count-->{win_count}')
    print(f'loss_count-->{loss_count}')
    win_rate = win_count / (win_count+loss_count) if (win_count+loss_count) != 0 else 0
    print(f'胜率为-->{win_rate * 100:.2f}%')
    return win_rate

# 计算盈亏比
def calculate_ror(data):
    # 步骤1: 计算 strategy 和 Close 的乘积，并根据结果的正负分别存储
    data['strategy_close'] = data['returns_dis'] * data['Close'] * data['position'].shift(1)
    positive_values = data[data['strategy_close'] > 0]['strategy_close']
    negative_values = data[data['strategy_close'] < 0]['strategy_close']

    # 步骤2: 分别计算正数和负数的平均值
    average_positive = positive_values.mean() if not positive_values.empty else 0
    average_negative = negative_values.mean() if not negative_values.empty else 0

    # 步骤3: 计算盈亏比
    # 使用 -average_negative 来避免除以0的情况，如果负数平均值不为0
    risk_reward_ratio = average_positive / (-1 * average_negative) if average_negative != 0 else float('inf')

    # 打印结果
    print(f'盈利平均值: {average_positive}')
    print(f'亏损平均值: {average_negative}')
    print(f'盈亏比: {risk_reward_ratio:.2f}')
    return risk_reward_ratio

# 计算最大回撤
def calculate_max_drawdown(data):
    # 计算策略的累计收益
    data['cumulative_returns'] = data['strategy'].cumsum().apply(np.exp)
    # 计算最高点
    data['peak'] = data['cumulative_returns'].cummax()
    # 计算最低点
    data['trough'] = data['cumulative_returns'].cummin()
    # 计算回撤
    data['drawdown'] = (data['peak'] - data['cumulative_returns']) / data['peak']
    # 找出最大回撤
    max_drawdown = data['drawdown'].max() * 100  # 转换为百分比形式
    print(f"最大回撤: {max_drawdown:.2f}%")
    return max_drawdown

# 计算夏普比率
def calculate_sharpe_ratio(data, risk_free_rate):
    # 计算平均收益
    mean_return = data['strategy'].mean()
    # 计算标准差，即总风险
    std_dev = data['strategy'].std()
    # 计算夏普比率，年化收益与无风险利率之差除以标准差
    sharpe_ratio = (mean_return - risk_free_rate) / std_dev
    print(f'夏普比率: {sharpe_ratio}')
    return sharpe_ratio

# 波动率计算
def calculate_volatility(data, window_size=252):
    # 计算日收益率的标准差
    volatility = data['returns'].std(ddof=1) * np.sqrt(window_size)
    print(f'股票年化波动率: {volatility:.2f}%')
    return volatility



if __name__ == '__main__':
    ticker = "002558.SZ"
    start_date = "2024-01-01"
    end_date = "2024-08-16"
    data = yf.Ticker(ticker).history(period="max", interval="1d",
                                     start=start_date, end=end_date, prepost=False,
                                     actions=False, auto_adjust=False,
                                     back_adjust=False, proxy=None,
                                     rounding=False, many=True)
    print(data)

    # 1、画出5日均线、10如均线和收盘价
    data['SMA_5'] = data['Close'].rolling(5).mean()
    data['SMA_10'] = data['Close'].rolling(10).mean()
    data[['Close', 'SMA_5', 'SMA_10']].plot(figsize=(10, 6))  # 可视化
    plt.title('Stock Close Price and SMA')  # 添加图表标题
    plt.xlabel('Date')  # 添加x轴标签
    plt.ylabel('Price')  # 添加y轴标签
    plt.show()  # 显示图表

    # 计算股票return
    data['returns'] = np.log(data['Close'] / data['Close'].shift(1))
    # Numpy向量化操作，避免循环；
    data['returns_dis'] = data['Close'] / data['Close'].shift(1) - 1
    data['position'] = np.where(data['SMA_5'] > data['SMA_10'], 1, 0)

    data.dropna(inplace=True)  # 去掉空值，NaN

    # 可视化；计算累计收益，连续下的算法；

    data['strategy'] = data['position'].shift(1) * data['returns']
    # 注意未来函数；一般会使得回测收益高估；

    sum_returns = data['returns'].cumsum().apply(np.exp)
    sum_strategy = data['strategy'].cumsum().apply(np.exp)
    print(f"Sum of 'returns': {sum_returns}")
    print(f"Sum of 'strategy': {sum_strategy}")

    data[['returns', 'strategy']].cumsum().apply(np.exp).plot(figsize=(10, 6))  # 可视化；离散的计算方法参考Momoentum策略

    # 找出所有买入点的日期
    buy_dates_index = data.index[data['position'] == 1]
    # 获取买入点的累计策略收益
    buy_strategy_values = sum_strategy[buy_dates_index]
    # 在折线图上标记买入点
    plt.scatter(buy_dates_index, buy_strategy_values, color='green', label='Buy', zorder=5, s=5)
    # 确保图例不遮挡标记点
    plt.legend(loc='upper left')

    plt.xlabel('Date')  # 添加x轴标签
    plt.ylabel('Cumulative Returns')  # 添加y轴标签
    plt.show()  # 显示图表

    # 调用函数计算胜率
    calculate_win_rate(data)
    # 调用新函数计算盈亏比
    calculate_ror(data)
    # 调用函数计算最大回撤
    calculate_max_drawdown(data)
    # 计算夏普比率
    risk_free_rate = 0.03  # 假设无风险利率为3%
    calculate_sharpe_ratio(data, risk_free_rate)

    data.to_csv(f'{ticker}.csv', index=True, encoding='utf-8-sig')



