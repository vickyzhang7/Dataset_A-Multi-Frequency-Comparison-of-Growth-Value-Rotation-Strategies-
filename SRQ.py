import pandas as pd
import numpy as np

# 读取CSV文件
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SPY_Q.csv'
df = pd.read_csv(file_path)

# 转换为时间索引（假设有日期列，否则可以跳过）
# df['Date'] = pd.to_datetime(df['Date'])
# df.set_index('Date', inplace=True)

# 年化无风险利率（美国）
rf_annual = 0  # 2.56%

# 计算季度收益率
returns = df[['Strong', 'Weak', 'SPY', 'SPYG', 'SPYV']].pct_change().dropna()

# 存储结果
results = {}

for col in returns.columns:
    quarterly_returns = returns[col]

    # 年化收益率（几何平均）
    total_return = (1 + quarterly_returns).prod()
    num_quarters = len(quarterly_returns)
    annual_return = total_return ** (4 / num_quarters) - 1

    # 年化波动率
    std_annual = quarterly_returns.std() * np.sqrt(4)

    # 夏普比率
    sharpe_ratio = (annual_return - rf_annual) / std_annual

    results[col] = {
        '年化收益率': annual_return,
        '年化标准差': std_annual,
        '夏普比率': sharpe_ratio
    }

# 打印结果
print("美国市场指数年化表现（基于季度数据）")
print("-" * 50)
for name, metrics in results.items():
    print(f"{name}:")
    print(f"  年化收益率: {metrics['年化收益率']:.2%}")
    print(f"  年化标准差: {metrics['年化标准差']:.2%}")
    print(f"  夏普比率: {metrics['夏普比率']:.4f}")
    print("-" * 50)
