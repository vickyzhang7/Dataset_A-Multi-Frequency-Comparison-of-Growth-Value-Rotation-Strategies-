import pandas as pd
import numpy as np

# === 参数设定 ===
rf_annual = 0  # 年化无风险利率（2.56%）
file_path = "/Users/xiaohuidexiaojiaoqi/Desktop/SPY_M.csv"

# === 读取数据 ===
df = pd.read_csv(file_path)

# 确保时间序列按时间升序排列（如果有日期列）
# 如果没有日期列，可以跳过这一步
# df['Date'] = pd.to_datetime(df['Date'])
# df.sort_values('Date', inplace=True)

# 选择需要计算的列
assets = ['Strong', 'Weak', 'SPY', 'SPYG', 'SPYV']
prices = df[assets]

# === 计算月度收益率 ===
monthly_returns = prices.pct_change().dropna()

# === 计算年化收益率 ===
# 公式：年化收益率 = (最终价格 / 初始价格)^(12 / 月数) - 1
num_months = len(prices) - 1
annual_returns = (prices.iloc[-1] / prices.iloc[0]) ** (12 / num_months) - 1

# === 计算年化标准差 ===
monthly_std = monthly_returns.std()
annual_std = monthly_std * np.sqrt(12)

# === 计算 Sharpe 比率 ===
sharpe_ratios = (annual_returns - rf_annual) / annual_std

# === 汇总结果 ===
results = pd.DataFrame({
    'Annual Return': annual_returns,
    'Annual Std Dev': annual_std,
    'Sharpe Ratio': sharpe_ratios
})

# 输出结果
print("=== 美国市场（年化收益率、年化标准差、夏普比率） ===")
print(results.round(4))
