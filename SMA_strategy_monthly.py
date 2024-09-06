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
ticker = '301171.SZ'
start_date = "2024-01-01"
end_date = "2024-08-16"
data = yf.Ticker(ticker).history(period="max", interval='1mo',
                                     start=start_date, end=end_date, prepost=False,
                                     actions=False, auto_adjust=False,
                                     back_adjust=False, proxy=None,
                                     rounding=False, many=True)

print(data)
