import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 文件路径
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/Summary.csv'
df = pd.read_csv(file_path, header=0)

# 横坐标标签
frequencies = ['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Semiannual', 'Annual']
x = np.arange(len(frequencies))

# 限定5种颜色（蓝、绿、红、橙、紫），红色在第3个，绿色在第2个
custom_colors = ['#1f77b4', '#2ca02c', '#d62728', '#ff7f0e', '#9467bd']

# ✅ 第一组策略（第1~5行）
strategies_1 = df.iloc[0:5, 0].tolist()
values_1 = df.iloc[0:5, 1:7].astype(str).apply(lambda row: row.str.rstrip('%').astype(float) / 100, axis=1).values

plt.figure(figsize=(12, 6))
bar_width = 0.8 / len(strategies_1)

for i in range(len(strategies_1)):
    plt.bar(x + i * bar_width, values_1[i], width=bar_width, color=custom_colors[i % 5], label=strategies_1[i])

plt.xticks(x + 0.4 - bar_width / 2, frequencies, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Frequency', fontsize=14)
plt.ylabel('Annual Average Drawdown', fontsize=14)
#plt.title('Annual Average Drawdown by Frequency and Strategy (US Stock Market)', fontsize=18)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# ✅ 第二组策略（第6~10行）
strategies_2 = df.iloc[5:10, 0].tolist()
values_2 = df.iloc[5:10, 1:7].astype(str).apply(lambda row: row.str.rstrip('%').astype(float) / 100, axis=1).values

plt.figure(figsize=(12, 6))
bar_width = 0.8 / len(strategies_2)

for i in range(len(strategies_2)):
    plt.bar(x + i * bar_width, values_2[i], width=bar_width, color=custom_colors[i % 5], label=strategies_2[i])

plt.xticks(x + 0.4 - bar_width / 2, frequencies, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Frequency', fontsize=14)
plt.ylabel('Annual Average Drawdown', fontsize=14)
#plt.title('Annual Average Drawdown by Frequency and Strategy (China Stock Market)', fontsize=18)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
