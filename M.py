import pandas as pd

# 读取月度数据
df_month = pd.read_csv('/Users/xiaohuidexiaojiaoqi/Desktop/SSE_M.csv')

# 转换为浮点数
for col in ['G', 'V', 'SS']:
    df_month[col] = pd.to_numeric(df_month[col], errors='coerce')

# 丢弃缺失值
df_month.dropna(subset=['G', 'V', 'SS'], inplace=True)

# --- 策略 1：Buy-and-Hold on SSCE ---
capital_ssce_m = 100
df_month['ssce_cum'] = (1 + df_month['SS']).cumprod()
final_ssce_m = capital_ssce_m * df_month['ssce_cum'].iloc[-1]

# --- 策略 2：Buy-and-Hold on Value (V) ---
capital_value_m = 100
df_month['v_cum'] = (1 + df_month['V']).cumprod()
final_value_m = capital_value_m * df_month['v_cum'].iloc[-1]

# --- 策略 3：Buy-and-Hold on Growth (G) ---
capital_growth_m = 100
df_month['g_cum'] = (1 + df_month['G']).cumprod()
final_growth_m = capital_growth_m * df_month['g_cum'].iloc[-1]

# --- 策略 4：Switching (买输者) ---
capital_switch_loser_m = 100
for i in range(len(df_month) - 1):
    g_today = df_month.loc[i, 'G']
    v_today = df_month.loc[i, 'V']
    if g_today > v_today:
        next_return = df_month.loc[i + 1, 'V']
    else:
        next_return = df_month.loc[i + 1, 'G']
    capital_switch_loser_m *= (1 + next_return)

# --- 策略 5：Switching (买赢家) ---
capital_switch_winner_m = 100
for i in range(len(df_month) - 1):
    g_today = df_month.loc[i, 'G']
    v_today = df_month.loc[i, 'V']
    if g_today > v_today:
        next_return = df_month.loc[i + 1, 'G']
    else:
        next_return = df_month.loc[i + 1, 'V']
    capital_switch_winner_m *= (1 + next_return)

# --- 输出结果 ---
print("\n--- Monthly ---")
print(f"SSEC Buy-and-Hold strategy final capital: {final_ssce_m:.2f}")
print(f"Value Buy-and-Hold strategy final capital: {final_value_m:.2f}")
print(f"Growth Buy-and-Hold strategy final capital: {final_growth_m:.2f}")
print(f"Switching strategy (buy weak performer next month) final capital: {capital_switch_loser_m:.2f}")
print(f"Switching strategy (buy strong performer next month) final capital: {capital_switch_winner_m:.2f}")
