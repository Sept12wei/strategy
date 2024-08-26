from SMA_strategy import *
from datetime import datetime
from datetime import datetime, timedelta

# 获取当前日期并格式化为字符串，格式为YYYY-MM-DD
current_date = datetime.now().strftime('%Y-%m-%d')
# 创建一个timedelta对象，表示一天的时间
one_day = timedelta(days=1)
# 计算当前日期的下一天
next_day = datetime.strptime(current_date, '%Y-%m-%d') + one_day
next_day_str = next_day.strftime('%Y-%m-%d')

risk_free_rate = 0.03
start_date = "2024-01-01"
end_date = next_day_str
print(current_date)

if __name__ == '__main__':
    file_path = './竞价交易策略.xlsx'
    df = pd.read_excel(file_path, engine='openpyxl')
    second_column_data = df['代码']
    print(second_column_data)

    # 创建一个空的DataFrame来存储结果
    results_df = pd.DataFrame(columns=['股票代码', '胜率', '盈亏比', '最大回撤', '夏普比率', '行业', 'position'])

    # 遍历第二列中的股票代码
    for stock_code in df['代码']:
        old_code = stock_code
        if stock_code.startswith('SH'):
            stock_code = f"{stock_code[2:]}.{'SS'}"
        elif stock_code.startswith('SZ'):
            stock_code = f"{stock_code[2:]}.{'SZ'}"
        print(stock_code)

        data = plot_stock_strategy(stock_code, start_date, end_date)

        # 将股票代码和指标数据作为一个新行添加到结果DataFrame中
        results_df = results_df.append({
            '股票代码': stock_code,
            '胜率': calculate_win_rate(data),
            '盈亏比': calculate_ror(data),
            '最大回撤': calculate_max_drawdown(data),
            '夏普比率': calculate_sharpe_ratio(data, risk_free_rate),
            '行业': df.loc[df['代码'] == f'{old_code}', '所属行业'].values[0],
            'position' : data['position'].iloc[-1]
        }, ignore_index=True)

    # 将结果写入新的Excel文件
    output_file_path = './竞价交易.xlsx'
    results_df.to_excel(output_file_path, index=False, engine='openpyxl')

    print(f'指标数据已写入 {output_file_path}')



