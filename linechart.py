import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/Summary.csv'
df = pd.read_csv(file_path, header=None)

# 横坐标标签
timeframes = df.iloc[0, 1:].tolist()
x = np.arange(len(timeframes))  # 横轴数值

# SPY 数据（行 2–4）
spy_labels = ['Buy & Hold', 'Buy Strong', 'Buy Weak']
spy_data = df.iloc[1:4, 1:].astype(float).values

# SSEC 数据（行 5–7）
ssec_labels = ['Buy & Hold', 'Buy Strong', 'Buy Weak']
ssec_data = df.iloc[4:7, 1:].astype(float).values

# ----------- SPY 折线图 -----------
plt.figure(figsize=(10, 6))

# Buy & Hold 平均值作为一条横线
spy_bh_avg = spy_data[0].mean()
plt.plot(x, [spy_bh_avg]*len(x), linestyle='--', color='gray', label='Buy & Hold (avg)', linewidth=2)

# 绘制另外两条折线
plt.plot(x, spy_data[1], marker='o', label='Buy Strong')
plt.plot(x, spy_data[2], marker='o', label='Buy Weak')

plt.xticks(x, timeframes)
plt.title('SPY Strategy Performance')
plt.ylabel('Returns')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------- SSEC 折线图 -----------
plt.figure(figsize=(10, 6))

# Buy & Hold 平均值作为一条横线
ssec_bh_avg = ssec_data[0].mean()
plt.plot(x, [ssec_bh_avg]*len(x), linestyle='--', color='gray', label='Buy & Hold (avg)', linewidth=2)

# 绘制另外两条折线
plt.plot(x, ssec_data[1], marker='o', label='Buy Strong')
plt.plot(x, ssec_data[2], marker='o', label='Buy Weak')

plt.xticks(x, timeframes)
plt.title('SSEC Strategy Performance')
plt.ylabel('Returns')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
