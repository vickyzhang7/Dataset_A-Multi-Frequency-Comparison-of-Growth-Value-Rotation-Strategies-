import pandas as pd
import numpy as np
import os

# 设定文件路径
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SSE_VG.csv'

# 读取 CSV 文件
df = pd.read_csv(file_path)

# 确保是按时间顺序排列（假设第一个是最早的）
df = df.sort_index()

# 提取价格列（5个投资组合）
columns = ['Strong', 'Weak', 'SSEC', 'GPrice', 'VPrice']
price_data = df[columns]

# 计算日度收益率
returns_daily = price_data.pct_change().dropna()

# 年化参数设定
trading_days_per_year = 252
years = 10
rf_annual = 0  # 3.01%

# 初始投资金额
initial_investment = 100

# 最终余额（用户提供）
final_balance = {
    'Strong': 150.3,
    'Weak': 53.4,
    'SSEC': 103.6,
    'GPrice': 99.5,
    'VPrice': 85.2
}

# 创建结果容器
results = []

for col in columns:
    # 计算年化收益率（CAGR）
    cagr = (final_balance[col] / initial_investment) ** (1 / years) - 1

    # 计算年化波动率（日波动率 × sqrt(252)）
    std_daily = returns_daily[col].std()
    std_annual = std_daily * np.sqrt(trading_days_per_year)

    # 计算 Sharpe 比率
    sharpe = (cagr - rf_annual) / std_annual if std_annual > 0 else np.nan

    results.append({
        '投资组合': col,
        '年化收益率': round(cagr * 100, 2),
        '年化标准差': round(std_annual * 100, 2),
        '夏普比率': round(sharpe, 3)
    })

# 转为 DataFrame 显示结果
results_df = pd.DataFrame(results)
print(results_df)
