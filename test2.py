import pandas as pd
import numpy as np

# 年化无风险利率
rf_annual = 0.0301
initial_value = 100
years = 10

# 你提供的最终余额
balances = {
    'Strong': 131.3,
    'Weak': 90.7,
    'SSEC': 87.0,
    'GPrice': 98.2,
    'VPrice': 106.5
}

# CSV 文件路径（10年共120个月的价格序列）
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SSE_A.csv'

# 读取数据
df = pd.read_csv(file_path)

# 如果有日期列，先排序
if 'Date' in df.columns:
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')

results = []

for column in df.columns:
    if column == 'Date':
        continue

    prices = df[column].dropna()
    if len(prices) < 2:
        continue

    # 月度收益率
    monthly_returns = prices.pct_change().dropna()

    # 年化标准差
    annual_std = monthly_returns.std() * np.sqrt(1)

    # 年化收益率（由 balance 反推）
    if column in balances:
        final_balance = balances[column]
        annual_return = (final_balance / initial_value) ** (1 / years) - 1

        # Sharpe Ratio
        sharpe_ratio = (annual_return - rf_annual) / annual_std if annual_std != 0 else np.nan

        results.append({
            'Index': column,
            'Annual Return (%)': round(annual_return * 100, 2),
            'Annual Std (%)': round(annual_std * 100, 2),
            'Sharpe Ratio': round(sharpe_ratio, 3)
        })

# 输出结果 DataFrame
result_df = pd.DataFrame(results).sort_values(by='Sharpe Ratio', ascending=False)
print(result_df.to_string(index=False))
