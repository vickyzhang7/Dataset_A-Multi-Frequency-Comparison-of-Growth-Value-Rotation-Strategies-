import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 读取数据
file_path = '/Users/xiaohuidexiaojiaoqi/Desktop/Sum2.csv'
df = pd.read_csv(file_path, header=None)

# 公共变量
strategies = df.iloc[1:11, 0].tolist()
colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
]

### 第一张图：策略在不同频率下的收益柱状图
frequencies = df.iloc[0, 1:7].tolist()
returns = df.iloc[1:11, 1:7].astype(float).values

plt.figure(figsize=(12, 6))
x = np.arange(len(frequencies))
bar_width = 0.8 / len(strategies)

for i in range(len(strategies)):
    plt.bar(x + i * bar_width, returns[i], width=bar_width, color=colors[i], label=strategies[i])

plt.xticks(x + 0.4 - bar_width / 2, frequencies)
plt.xlabel('Frequency')
plt.ylabel('Return')
plt.title('Return by Frequency and Strategy')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# 第二张图：平均回撤柱状图（图例放右侧，隐藏x轴文字）
drawdowns = df.iloc[1:11, 7].astype(str).str.rstrip('%').astype(float).values / 100

plt.figure(figsize=(12, 6))
x = np.arange(len(strategies))
bars = plt.bar(x, drawdowns, color=colors)

# 设置图例，右上角外部
for i, bar in enumerate(bars):
    bar.set_label(strategies[i])
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

# 隐藏x轴刻度文字，只保留图例
plt.xticks(x, [''] * len(strategies))

# 设置 y 轴刻度范围及间隔（从-40%到0，步长为5%）
yticks = np.arange(-0.40, 0.01, 0.05)
plt.yticks(yticks, [f'{int(y*100)}%' for y in yticks])

# 添加数值标签
for bar in bars:
    y = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, y - 0.005, f'{y:.1%}', ha='center', va='top', fontsize=10)

plt.title('Average Drawdown by Strategy')
plt.ylabel('Drawdown (%)')
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
