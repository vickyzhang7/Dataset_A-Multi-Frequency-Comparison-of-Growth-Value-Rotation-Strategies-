import pandas as pd
import numpy as np

# 读取数据
ssec_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SSE_VG.csv'
spy_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SPY_D.csv'

df_ssec = pd.read_csv(ssec_path)
df_spy = pd.read_csv(spy_path)

# 转换日期格式并排序
df_ssec['Date'] = pd.to_datetime(df_ssec['Date'], format="%m/%d/%y")
df_spy['Date'] = pd.to_datetime(df_spy['Date'], format="%m/%d/%y")

df_ssec.sort_values('Date', inplace=True)
df_spy.sort_values('Date', inplace=True)

# Drawdown 计算函数
def average_annual_drawdown(prices, dates):
    df = pd.DataFrame({'Price': prices.values, 'Year': dates.dt.year})
    annual_dd = []

    for year in df['Year'].unique():
        year_data = df[df['Year'] == year]['Price']
        if len(year_data) < 2:
            continue
        running_max = year_data.cummax()
        drawdowns = (year_data - running_max) / running_max
        annual_dd.append(drawdowns.min())

    return np.mean(annual_dd)

# 计算 6 个指标的年均最大回撤
results = {
    'SSEC': average_annual_drawdown(df_ssec['SSEC'], df_ssec['Date']),
    'SSEC Growth (GPrice)': average_annual_drawdown(df_ssec['GPrice'], df_ssec['Date']),
    'SSEC Value (VPrice)': average_annual_drawdown(df_ssec['VPrice'], df_ssec['Date']),
    'SPY': average_annual_drawdown(df_spy['SPY'], df_spy['Date']),
    'SPY Growth (SPYG)': average_annual_drawdown(df_spy['SPYG'], df_spy['Date']),
    'SPY Value (SPYV)': average_annual_drawdown(df_spy['SPYV'], df_spy['Date']),
}

# 输出结果
for name, dd in results.items():
    print(f'{name}: {dd:.2%}')

import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
ssec_df = pd.read_csv('/Users/xiaohuidexiaojiaoqi/Desktop/SSE_VG.csv')
spy_df = pd.read_csv('/Users/xiaohuidexiaojiaoqi/Desktop/SPY_D.csv')

ssec_df['Date'] = pd.to_datetime(ssec_df['Date'], format="%m/%d/%y")
spy_df['Date'] = pd.to_datetime(spy_df['Date'], format="%m/%d/%y")

# 构建 Strong 和 Weak 列
ssec_df['SSEC_Strong'] = ssec_df.apply(lambda row: row['GPrice'] if row['G'] > row['V'] else row['VPrice'], axis=1)
ssec_df['SSEC_Weak'] = ssec_df.apply(lambda row: row['VPrice'] if row['G'] > row['V'] else row['GPrice'], axis=1)

spy_df['SPY_Strong'] = spy_df.apply(lambda row: row['SPYG'] if row['G'] > row['V'] else row['SPYV'], axis=1)
spy_df['SPY_Weak'] = spy_df.apply(lambda row: row['SPYV'] if row['G'] > row['V'] else row['SPYG'], axis=1)

# 绘图
plt.figure(figsize=(12, 5))
plt.plot(ssec_df['Date'], ssec_df['SSEC_Strong'], label='SSEC Strong')
plt.plot(ssec_df['Date'], ssec_df['SSEC_Weak'], label='SSEC Weak')
plt.title('SSEC: Strong vs Weak')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()

plt.figure(figsize=(12, 5))
plt.plot(spy_df['Date'], spy_df['SPY_Strong'], label='SPY Strong')
plt.plot(spy_df['Date'], spy_df['SPY_Weak'], label='SPY Weak')
plt.title('SPY: Strong vs Weak')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()


# Drawdown 函数
def calculate_annual_average_drawdown(price_series, dates):
    df = pd.DataFrame({'Price': price_series, 'Date': pd.to_datetime(dates)})
    df.set_index('Date', inplace=True)
    df['Peak'] = df['Price'].cummax()
    df['Drawdown'] = (df['Price'] - df['Peak']) / df['Peak']
    drawdown_by_year = df['Drawdown'].groupby(df.index.year).mean()
    return drawdown_by_year.mean()


# 计算并输出 drawdown
ssec_strong_dd = calculate_annual_average_drawdown(ssec_df['SSEC_Strong'], ssec_df['Date'])
ssec_weak_dd = calculate_annual_average_drawdown(ssec_df['SSEC_Weak'], ssec_df['Date'])
spy_strong_dd = calculate_annual_average_drawdown(spy_df['SPY_Strong'], spy_df['Date'])
spy_weak_dd = calculate_annual_average_drawdown(spy_df['SPY_Weak'], spy_df['Date'])

print(f"SSEC Strong Annual Avg Drawdown: {ssec_strong_dd:.2%}")
print(f"SSEC Weak Annual Avg Drawdown: {ssec_weak_dd:.2%}")
print(f"SPY Strong Annual Avg Drawdown: {spy_strong_dd:.2%}")
print(f"SPY Weak Annual Avg Drawdown: {spy_weak_dd:.2%}")
