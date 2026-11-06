import pandas as pd

# 读取数据
df = pd.read_csv('/Users/xiaohuidexiaojiaoqi/Desktop/SSE_VG.csv')

# 转换为浮点数
for col in ['G', 'V', 'SS']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# 丢弃缺失值
df.dropna(subset=['G', 'V', 'SS'], inplace=True)

# --- 策略 1：Buy-and-Hold on SSCE ---
capital_ssce = 100
df['ssce_cum'] = (1 + df['SS']).cumprod()
final_ssce = capital_ssce * df['ssce_cum'].iloc[-1]

# --- 策略 2：Buy-and-Hold on Value (V) ---
capital_value = 100
df['v_cum'] = (1 + df['V']).cumprod()
final_value = capital_value * df['v_cum'].iloc[-1]

# --- 策略 3：Buy-and-Hold on Growth (G) ---
capital_growth = 100
df['g_cum'] = (1 + df['G']).cumprod()
final_growth = capital_growth * df['g_cum'].iloc[-1]

# --- 策略 4：Switching (买输者) ---
capital_switch_loser = 100
for i in range(len(df) - 1):
    g_today = df.loc[i, 'G']
    v_today = df.loc[i, 'V']
    if g_today > v_today:
        next_return = df.loc[i + 1, 'V']
    else:
        next_return = df.loc[i + 1, 'G']
    capital_switch_loser *= (1 + next_return)

# --- 策略 5：Switching (买赢家) ---
capital_switch_winner = 100
for i in range(len(df) - 1):
    g_today = df.loc[i, 'G']
    v_today = df.loc[i, 'V']
    if g_today > v_today:
        next_return = df.loc[i + 1, 'G']
    else:
        next_return = df.loc[i + 1, 'V']
    capital_switch_winner *= (1 + next_return)

# --- 输出结果 ---
print("\n--- Daily ---")
print(f"SSEC Buy-and-Hold strategy final capital: {final_ssce:.2f}")
print(f"Value Buy-and-Hold strategy final capital: {final_value:.2f}")
print(f"Growth Buy-and-Hold strategy final capital: {final_growth:.2f}")
print(f"Switching strategy (buy weak performer next day) final capital: {capital_switch_loser:.2f}")
print(f"Switching strategy (buy strong performer next day) final capital: {capital_switch_winner:.2f}")
