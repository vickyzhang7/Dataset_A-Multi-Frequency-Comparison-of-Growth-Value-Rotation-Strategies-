import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

path_spy = '/Users/xiaohuidexiaojiaoqi/Desktop/SPY_Q.csv'
path_sse = '/Users/xiaohuidexiaojiaoqi/Desktop/SSE_Q.csv'


# 先按字符串读，parse_dates=False
df_spy = pd.read_csv(path_spy, parse_dates=False)
df_sse = pd.read_csv(path_sse, parse_dates=False)

# 再转换日期列，格式是月/日/年 两位年
df_spy['Date'] = pd.to_datetime(df_spy['Date'], format='%m/%d/%y', errors='coerce')
df_sse['Date'] = pd.to_datetime(df_sse['Date'], format='%m/%d/%y', errors='coerce')

# 时间范围，2015-06末 到 2025-03末，每3个月（末日）
date_range = pd.date_range(start='2015-06-30', periods=40, freq='3ME')

plt.figure(figsize=(14,6))
for col in ['SPY', 'SPYG', 'SPYV', 'Strong', 'Weak']:
    series = df_spy.set_index('Date')[col].reindex(date_range).interpolate()
    plt.plot(date_range, series, label=col)
plt.title('SPY Quarterly Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(date_range[::4], date_range[::4].strftime('%Y-%m'), rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(14,6))
for col in ['SSEC', 'GPrice', 'VPrice', 'Strong', 'Weak']:
    series = df_sse.set_index('Date')[col].reindex(date_range).interpolate()
    plt.plot(date_range, series, label=col)
plt.title('SSE Quarterly Prices')
plt.xlabel('Date')
plt.ylabel('Price')
plt.xticks(date_range[::4], date_range[::4].strftime('%Y-%m'), rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
