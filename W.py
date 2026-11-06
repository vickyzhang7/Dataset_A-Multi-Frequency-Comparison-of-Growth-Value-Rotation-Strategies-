import pandas as pd

# 读取周度数据
df_week = pd.read_csv('/Users/xiaohuidexiaojiaoqi/Desktop/SSE_W.csv')


# 转换为浮点数
for col in ['G', 'V', 'SS']:
    df_week[col] = pd.to_numeric(df_week[col], errors='coerce')

# 丢弃缺失值
df_week.dropna(subset=['G', 'V', 'SS'], inplace=True)

# --- 策略 1：Buy-and-Hold on SSCE ---
capital_ssce_w = 100
df_week['ssce_cum'] = (1 + df_week['SS']).cumprod()
final_ssce_w = capital_ssce_w * df_week['ssce_cum'].iloc[-1]

# --- 策略 2：Buy-and-Hold on Value (V) ---
capital_value_w = 100
df_week['v_cum'] = (1 + df_week['V']).cumprod()
final_value_w = capital_value_w * df_week['v_cum'].iloc[-1]

# --- 策略 3：Buy-and-Hold on Growth (G) ---
capital_growth_w = 100
df_week['g_cum'] = (1 + df_week['G']).cumprod()
final_growth_w = capital_growth_w * df_week['g_cum'].iloc[-1]

# --- 策略 4：Switching (买输者) ---
capital_switch_loser_w = 100
for i in range(len(df_week) - 1):
    g_today = df_week.loc[i, 'G']
    v_today = df_week.loc[i, 'V']
    if g_today > v_today:
        next_return = df_week.loc[i + 1, 'V']
    else:
        next_return = df_week.loc[i + 1, 'G']
    capital_switch_loser_w *= (1 + next_return)

# --- 策略 5：Switching (买赢家) ---
capital_switch_winner_w = 100
for i in range(len(df_week) - 1):
    g_today = df_week.loc[i, 'G']
    v_today = df_week.loc[i, 'V']
    if g_today > v_today:
        next_return = df_week.loc[i + 1, 'G']
    else:
        next_return = df_week.loc[i + 1, 'V']
    capital_switch_winner_w *= (1 + next_return)

# --- 输出结果 ---
print("\n--- Weekly ---")
print(f"SSEC Buy-and-Hold strategy final capital: {final_ssce_w:.2f}")
print(f"Value Buy-and-Hold strategy final capital: {final_value_w:.2f}")
print(f"Growth Buy-and-Hold strategy final capital: {final_growth_w:.2f}")
print(f"Switching strategy (buy weak performer next week) final capital: {capital_switch_loser_w:.2f}")
print(f"Switching strategy (buy strong performer next week) final capital: {capital_switch_winner_w:.2f}")
