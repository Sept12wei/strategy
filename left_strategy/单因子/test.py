import numpy as np
import pandas as pd
import yfinance as yf

df = pd.read_excel('./股票列表.xlsx', engine='openpyxl')


code_list = []
# 遍历第二列中的股票代码
for stock_code in df['代码']:
    old_code = stock_code
    if stock_code.startswith('SH'):
        stock_code = f"{stock_code[2:]}.{'SS'}"
    elif stock_code.startswith('SZ'):
        stock_code = f"{stock_code[2:]}.{'SZ'}"
    code_list.append(stock_code)


ticker = '300736.SZ'
start_date = "2015-01-01"
end_date = "2024-08-31"

all_data = pd.DataFrame()
for ticker in code_list[0:10]:
    data = yf.Ticker(ticker).history(period="max", interval="1d",
                                     start=start_date, end=end_date, prepost=False,
                                     actions=False, auto_adjust=False,
                                     back_adjust=False, proxy=None,
                                     rounding=False, many=True)
    data['code'] = ticker
    all_data = pd.concat([all_data, data])  # 将数据添加到 all_data 中


print(all_data)
all_data.to_csv('all_data.csv')