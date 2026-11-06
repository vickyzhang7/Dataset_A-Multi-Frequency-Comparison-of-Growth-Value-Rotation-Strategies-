import pandas as pd
import numpy as np

# 文件路径
file_path = "/Users/xiaohuidexiaojiaoqi/Desktop/SPY_D.csv"

# 读取数据
df = pd.read_csv(file_path)

# 确保日期列存在并转为 datetime（假设叫 'Date'，否则你改列名）
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    df.set_index('Date', inplace=True)

# 你感兴趣的列
columns = ['Strong', 'Weak', 'SPY', 'SPYG', 'SPYV']

# 年化无风险利率（美国）
risk_free_rate = 0 # 2.56%

# 用收盘价计算月度或日度收益率（这里假设数据是日度的）
returns = df[columns].pct_change().dropna()

# 计算年数（从数据长度和频率中推测）
days = (df.index[-1] - df.index[0]).days
years = days / 365.25

results = {}

for col in columns:
    prices = df[col].dropna()
    start_price = prices.iloc[0]
    end_price = prices.iloc[-1]

    # 年化收益率（CAGR）
    cagr = (end_price / start_price) ** (1 / years) - 1

    # 年化波动率（用日收益乘以√252）
    volatility = returns[col].std() * np.sqrt(252)

    # 夏普比率
    sharpe_ratio = (cagr - risk_free_rate) / volatility

    results[col] = {
        'Annual Return (CAGR)': cagr,
        'Annual Std Dev': volatility,
        'Risk-Free Rate': risk_free_rate,
        'Sharpe Ratio': sharpe_ratio
    }

# 输出结果
print("\n=== Sharpe Ratio Summary (U.S. Market) ===")
for asset, metrics in results.items():
    print(f"\n{asset}:")
    print(f"  Annual Return (CAGR): {metrics['Annual Return (CAGR)']:.2%}")
    print(f"  Annual Std Dev     : {metrics['Annual Std Dev']:.2%}")
    print(f"  Risk-Free Rate     : {metrics['Risk-Free Rate']:.2%}")
    print(f"  Sharpe Ratio       : {metrics['Sharpe Ratio']:.4f}")
