import pandas as pd
import numpy as np
import os

# 参数
rf_annual = 0  # 年化无风险利率（3.01%）
initial_investment = 100
years = 10
weeks_per_year = 52

# 读取数据
file_path = "/Users/xiaohuidexiaojiaoqi/Desktop/SSE_W.csv"
df = pd.read_csv(file_path)

# 指数列名
indices = ['Strong', 'Weak', 'SSEC', 'GPrice', 'VPrice']

# 用于存储结果
results = []

for index in indices:
    prices = df[index].dropna()

    # 1. 周收益率
    weekly_returns = prices.pct_change().dropna()

    # 2. 年化收益率（几何平均）
    total_return = prices.iloc[-1] / prices.iloc[0]
    annual_return = total_return ** (1 / years) - 1

    # 3. 年化波动率
    std_weekly = np.std(weekly_returns)
    annual_std = std_weekly * np.sqrt(weeks_per_year)

    # 4. 夏普比率
    sharpe_ratio = (annual_return - rf_annual) / annual_std if annual_std != 0 else np.nan

    results.append({
        'Index': index,
        'Annual Return': annual_return,
        'Annual Std Dev': annual_std,
        'Sharpe Ratio': sharpe_ratio
    })

# 打印结果
result_df = pd.DataFrame(results)
pd.set_option('display.float_format', '{:.4f}'.format)
print(result_df)
