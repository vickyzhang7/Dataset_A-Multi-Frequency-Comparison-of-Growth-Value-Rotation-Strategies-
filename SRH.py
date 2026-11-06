import pandas as pd
import numpy as np

# === 1. 加载数据 ===
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SPY_H.csv'
df = pd.read_csv(file_path)

# 确保时间列存在（如果有），否则生成索引
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

# === 2. 计算半年度收益率 ===
returns = df.pct_change().dropna()  # 半年度收益率

# === 3. 参数设定 ===
rf_annual = 0  # 美国年化无风险利率
periods_per_year = 2  # 半年度：每年2期

# === 4. 计算指标 ===
results = {}

for col in returns.columns:
    # 半年度收益序列
    r = returns[col]

    # 年化收益率（几何平均）
    cumulative_return = (1 + r).prod()
    annual_return = cumulative_return ** (periods_per_year / len(r)) - 1

    # 年化波动率
    annual_vol = r.std() * np.sqrt(periods_per_year)

    # 年化 Sharpe 比率
    sharpe_ratio = (annual_return - rf_annual) / annual_vol if annual_vol > 0 else np.nan

    # 存储结果
    results[col] = {
        'Annual Return': annual_return,
        'Annual Volatility': annual_vol,
        'Sharpe Ratio': sharpe_ratio
    }

# === 5. 输出结果 ===
print("=== Performance Summary (Annualized) ===")
for asset, metrics in results.items():
    print(f"\n{asset}:")
    print(f"  年化收益率:     {metrics['Annual Return']:.2%}")
    print(f"  年化标准差:     {metrics['Annual Volatility']:.2%}")
    print(f"  夏普比率:       {metrics['Sharpe Ratio']:.4f}")
