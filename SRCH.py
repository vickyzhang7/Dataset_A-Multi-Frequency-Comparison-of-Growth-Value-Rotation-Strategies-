import pandas as pd
import numpy as np

# -------------------
# 基本参数
# -------------------
initial_investment = 100
years = 10
rf_annual = 0.0301  # 年化无风险利率（中国10年期国债）

# -------------------
# 10年后余额数据
# -------------------
final_balances = {
    'Strong': 140.3,
    'Weak': 71.0,
    'SSEC': 96.7,
    'GPrice': 100.8,
    'VPrice': 123.2
}

# -------------------
# 从 CSV 加载半年度数据
# -------------------
csv_path = '/Users/xiaohuidexiaojiaoqi/Desktop/SSE_H.csv'

half_year_data = pd.read_csv(csv_path)
half_year_data = half_year_data.apply(lambda col: pd.to_numeric(col, errors='coerce'))
half_year_data.dropna(how='all', axis=1, inplace=True)
half_year_data.dropna(how='any', axis=0, inplace=True)

# 去掉列名多余空格
half_year_data.columns = half_year_data.columns.str.strip()

# -------------------
# 定义计算函数
# -------------------
def calc_annualized_return(final_value, initial_value, years):
    return (final_value / initial_value) ** (1 / years) - 1

def calc_annualized_std(half_year_returns):
    return half_year_returns.std() * np.sqrt(2)  # 半年数据

def calc_half_year_returns(balance_series):
    return balance_series.pct_change().dropna()

def calc_sharpe_ratio(annual_return, annual_std, rf):
    return (annual_return - rf) / annual_std if annual_std > 0 else np.nan

# -------------------
# 汇总分析
# -------------------
results = {}

print("✅ CSV 列名:", half_year_data.columns.tolist())  # 调试用，确认列名

for product, final_value in final_balances.items():
    annual_return = calc_annualized_return(final_value, initial_investment, years)

    if product in half_year_data.columns:
        balance_series = half_year_data[product]
        half_year_returns = calc_half_year_returns(balance_series)
        annual_std = calc_annualized_std(half_year_returns)
        sharpe = calc_sharpe_ratio(annual_return, annual_std, rf_annual)
    else:
        annual_std = np.nan
        sharpe = np.nan

    results[product] = {
        'Annualized Return': annual_return,
        'Annualized Std Dev': annual_std,
        'Sharpe Ratio': sharpe
    }

# -------------------
# 打印结果
# -------------------
for product, metrics in results.items():
    print(f"📊 {product}")
    print(f"  年化收益率: {metrics['Annualized Return']:.4f} ({metrics['Annualized Return'] * 100:.2f}%)")
    if not np.isnan(metrics['Annualized Std Dev']):
        print(f"  年化标准差: {metrics['Annualized Std Dev']:.4f} ({metrics['Annualized Std Dev'] * 100:.2f}%)")
        print(f"  夏普比率: {metrics['Sharpe Ratio']:.4f}")
    else:
        print("  ⚠️ 无半年度数据，无法计算标准差和夏普比率")
    print()
