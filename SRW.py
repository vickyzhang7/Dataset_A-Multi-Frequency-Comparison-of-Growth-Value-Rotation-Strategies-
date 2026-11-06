import pandas as pd
import numpy as np

# ----------------------------
# 参数设置
# ----------------------------
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SPY_W.csv'
columns = ['Strong', 'Weak', 'SPY', 'SPYG', 'SPYV']
rf_annual = 0  # 年化无风险利率
weeks_per_year = 52

# ----------------------------
# 读取数据
# ----------------------------
df = pd.read_csv(file_path)

# 如果日期列存在并不是索引，可取消注释以下行
# df['Date'] = pd.to_datetime(df['Date'])
# df.set_index('Date', inplace=True)

# ----------------------------
# 计算每周收益率
# ----------------------------
returns = df[columns].pct_change().dropna()

# ----------------------------
# 初始化结果存储
# ----------------------------
results = []

# ----------------------------
# 对每个指数计算年化收益率、标准差和Sharpe比率
# ----------------------------
for col in columns:
    weekly_returns = returns[col]

    # 年化收益率（几何平均）
    cumulative_return = (1 + weekly_returns).prod()
    n_years = len(weekly_returns) / weeks_per_year
    annual_return = cumulative_return ** (1 / n_years) - 1

    # 年化波动率
    annual_std = weekly_returns.std() * np.sqrt(weeks_per_year)

    # 夏普比率
    sharpe_ratio = (annual_return - rf_annual) / annual_std

    results.append({
        'Index': col,
        'Annual Return (%)': annual_return * 100,
        'Annual Std Dev (%)': annual_std * 100,
        'Sharpe Ratio': sharpe_ratio
    })

# ----------------------------
# 输出结果
# ----------------------------
results_df = pd.DataFrame(results)
print(results_df.round(4))
