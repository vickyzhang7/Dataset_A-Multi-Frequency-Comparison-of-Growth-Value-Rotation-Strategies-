import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/Sum2.csv'
df = pd.read_csv(file_path, header=None)

# 公共变量
frequencies = df.iloc[0, 1:7].tolist()

# 限定颜色：蓝、绿、红、橙、紫
limited_colors = ['#1f77b4', '#2ca02c', '#d62728', '#ff7f0e', '#9467bd']

# 第1张图：第2到第6行策略（index 1 到 5）
strategies_1 = df.iloc[1:6, 0].tolist()
returns_1 = df.iloc[1:6, 1:7].astype(float).values

plt.figure(figsize=(12, 6))
x = np.arange(len(frequencies))
bar_width = 0.8 / len(strategies_1)

for i in range(len(strategies_1)):
    color = limited_colors[i % 5]
    plt.bar(x + i * bar_width, returns_1[i], width=bar_width, color=color, label=strategies_1[i])

plt.xticks(x + 0.4 - bar_width / 2, frequencies, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Frequency', fontsize=14)
plt.ylabel('Balance', fontsize=14)
plt.title('Balance by Frequency and Strategy (US Stock Market)', fontsize=18)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 第2张图：第7到第11行策略（index 6 到 10）
strategies_2 = df.iloc[6:11, 0].tolist()
returns_2 = df.iloc[6:11, 1:7].astype(float).values

plt.figure(figsize=(12, 6))
bar_width = 0.8 / len(strategies_2)

for i in range(len(strategies_2)):
    color = limited_colors[i % 5]
    plt.bar(x + i * bar_width, returns_2[i], width=bar_width, color=color, label=strategies_2[i])

plt.xticks(x + 0.4 - bar_width / 2, frequencies, fontsize=12)
plt.yticks(fontsize=12)
plt.xlabel('Frequency', fontsize=14)
plt.ylabel('Balance', fontsize=14)
plt.title('Balance by Frequency and Strategy (China Stock Market)', fontsize=18)
plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
