import os
import pandas as pd
import numpy as np

# 文件路径与文件名
folder_path = '/Users/xiaohuidexiaojiaoqi/Desktop'
file_names = [
    'SPY_WD.csv', 'SPY_MD.csv', 'SPY_QD.csv', 'SPY_HD.csv', 'SPY_AD.csv',
    'SSE_WD.csv', 'SSE_MD.csv', 'SSE_QD.csv', 'SSE_HD.csv', 'SSE_AD.csv'
]

def max_drawdown(series):
    """计算单个时间序列的最大回撤"""
    cummax = series.cummax()
    drawdown = (series - cummax) / cummax
    return drawdown.min()

def annual_mdd(df, col):
    """计算每年的最大回撤，返回每年值和平均值"""
    df['Year'] = df['Date'].dt.year
    result = {}
    for year, group in df.groupby('Year'):
        dd = max_drawdown(group[col])
        result[year] = dd
    avg_dd = np.mean(list(result.values()))
    return result, avg_dd

# 主处理逻辑
summary = []

for file in file_names:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, parse_dates=['Date'])
    df = df.sort_values('Date')

    strong_dds, strong_avg = annual_mdd(df, 'Strong')
    weak_dds, weak_avg = annual_mdd(df, 'Weak')

    summary.append({
        'File': file,
        'Strong Avg Annual MDD': strong_avg,
        'Weak Avg Annual MDD': weak_avg
    })

# 输出结果
result_df = pd.DataFrame(summary)
pd.set_option("display.float_format", "{:.2%}".format)
print(result_df)
