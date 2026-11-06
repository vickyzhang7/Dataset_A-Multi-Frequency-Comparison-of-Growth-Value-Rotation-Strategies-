import pandas as pd
import numpy as np

# 参数设置
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SPY_A.csv'
rf_annual = 0 # 美国年化无风险利率 2.56%

# 读取年度数据
df = pd.read_csv(file_path)

# 确保按时间排序（假设第一列是年份或日期）
df = df.sort_values(by=df.columns[0])

# 指数价格列
price_columns = ['Strong', 'Weak', 'SPY', 'SPYG', 'SPYV']

# 计算年度收益率（简单百分比变化）
returns = df[price_columns].pct_change().dropna()

# 计算年化指标（这里每个数据点就是一年的）
results = []

for col in price_columns:
    annual_returns = returns[col]

    # 年化收益率（几何）
    cumulative_return = (1 + annual_returns).prod()
    n_years = len(annual_returns)
    annual_return = cumulative_return ** (1 / n_years) - 1

    # 年化标准差（年度数据，直接取标准差）
    annual_std = annual_returns.std()

    # 夏普比率
    sharpe_ratio = (annual_return - rf_annual) / annual_std

    results.append({
        '指数': col,
        '年化收益率': round(annual_return * 100, 2),
        '年化标准差': round(annual_std * 100, 2),
        '夏普比率': round(sharpe_ratio, 3)
    })

# 输出结果表格
results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
