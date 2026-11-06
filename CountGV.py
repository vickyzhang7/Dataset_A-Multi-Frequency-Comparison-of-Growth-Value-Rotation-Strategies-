import pandas as pd
import os

# 文件列表
filenames = ['SPY_D.csv', 'SPY_W.csv', 'SPY_M.csv', 'SPY_Q.csv', 'SPY_H.csv', 'SPY_A.csv'
             ,'SSE_VG.csv', 'SSE_W.csv', 'SSE_M.csv', 'SSE_Q.csv', 'SSE_H.csv', 'SSE_A.csv']
folder_path = '/Users/xiaohuidexiaojiaoqi/Desktop'

# 处理每个文件
for fname in filenames:
    file_path = os.path.join(folder_path, fname)

    try:
        df = pd.read_csv(file_path)

        # 初始化计分列
        df['G_win'] = 0
        df['V_win'] = 0

        # 遍历行进行比较
        for i in range(len(df)):
            g = df.at[i, 'G']
            v = df.at[i, 'V']
            if pd.notna(g) and pd.notna(v):
                if g > v:
                    df.at[i, 'G_win'] = 1
                elif v > g:
                    df.at[i, 'V_win'] = 1

        # 统计总胜出次数
        g_total = df['G_win'].sum()
        v_total = df['V_win'].sum()

        print(f"{fname}: G:  {g_total} , V:  {v_total} ")

        # 如需保存结果文件（可选）
        # result_path = os.path.join(folder_path, fname.replace('.csv', '_result.csv'))
        # df.to_csv(result_path, index=False)

    except Exception as e:
        print(f"处理文件 {fname} 时出错: {e}")
