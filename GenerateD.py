'''
import pandas as pd
import os

# 设置基础路径和日期格式
base_path = "/Users/xiaohuidexiaojiaoqi/Desktop"
date_format = "%m/%d/%y"

# 文件名映射
frequencies = {
    "W": "Weekly",
    "M": "Monthly",
    "Q": "Quarterly",
    "H": "Semiannual",
    "A": "Annual"
}

# 加载日度数据
spy_d = pd.read_csv(f"{base_path}/SPY_D.csv", parse_dates=["Date"], date_format=date_format)
sse_d = pd.read_csv(f"{base_path}/SSE_VG.csv", parse_dates=["Date"], date_format=date_format)

# 遍历每种频率
for freq in frequencies.keys():
    spy_f = pd.read_csv(f"{base_path}/SPY_{freq}.csv", parse_dates=["Date"], date_format=date_format)
    sse_f = pd.read_csv(f"{base_path}/SSE_{freq}.csv", parse_dates=["Date"], date_format=date_format)

    spy_out_rows = []
    sse_out_rows = []

    for i in range(len(spy_f) - 1):
        start_date = spy_f.loc[i, "Date"]
        end_date = spy_f.loc[i + 1, "Date"] - pd.Timedelta(days=1)
        mask = (spy_d["Date"] >= start_date) & (spy_d["Date"] <= end_date)

        strong_val = spy_f.loc[i, "Strong"]
        weak_val = spy_f.loc[i, "Weak"]

        # 确定 SPYG/SPYV 来源
        if (spy_f.loc[i, "Strong"] == spy_f.loc[i, "SPYG"]):
            strong_col = "SPYG"
            weak_col = "SPYV"
        elif (spy_f.loc[i, "Strong"] == spy_f.loc[i, "SPYV"]):
            strong_col = "SPYV"
            weak_col = "SPYG"
        else:
            raise ValueError(f"SPY 第 {i} 行 Strong 值 {strong_val} 无匹配")

        segment = spy_d.loc[mask].copy()
        segment["Strong"] = segment[strong_col]
        segment["Weak"] = segment[weak_col]
        spy_out_rows.append(segment[["Date", "Strong", "Weak"]])

    for i in range(len(sse_f) - 1):
        start_date = sse_f.loc[i, "Date"]
        end_date = sse_f.loc[i + 1, "Date"] - pd.Timedelta(days=1)
        mask = (sse_d["Date"] >= start_date) & (sse_d["Date"] <= end_date)

        strong_val = sse_f.loc[i, "Strong"]
        weak_val = sse_f.loc[i, "Weak"]

        # 确定 GPrice/VPrice 来源
        if (sse_f.loc[i, "Strong"] == sse_f.loc[i, "GPrice"]):
            strong_col = "GPrice"
            weak_col = "VPrice"
        elif (sse_f.loc[i, "Strong"] == sse_f.loc[i, "VPrice"]):
            strong_col = "VPrice"
            weak_col = "GPrice"
        else:
            raise ValueError(f"SSE 第 {i} 行 Strong 值 {strong_val} 无匹配")

        segment = sse_d.loc[mask].copy()
        segment["Strong"] = segment[strong_col]
        segment["Weak"] = segment[weak_col]
        sse_out_rows.append(segment[["Date", "Strong", "Weak"]])

    # 拼接全部结果并导出
    spy_result = pd.concat(spy_out_rows)
    sse_result = pd.concat(sse_out_rows)

    spy_result.to_csv(f"{base_path}/SPY_{freq}D.csv", index=False)
    sse_result.to_csv(f"{base_path}/SSE_{freq}D.csv", index=False)
'''

import pandas as pd
import numpy as np
import os

# 设置基础路径和日期格式
base_path = "/Users/xiaohuidexiaojiaoqi/Desktop"
date_format = "%m/%d/%y"

# 文件名映射
frequencies = {
    "W": "Weekly",
    "M": "Monthly",
    "Q": "Quarterly",
    "H": "Semiannual",
    "A": "Annual"
}

# 加载日度数据
spy_d = pd.read_csv(f"{base_path}/SPY_D.csv", parse_dates=["Date"], date_format=date_format)
sse_d = pd.read_csv(f"{base_path}/SSE_VG.csv", parse_dates=["Date"], date_format=date_format)

# 遍历每种频率
for freq in frequencies.keys():
    spy_f = pd.read_csv(f"{base_path}/SPY_{freq}.csv", parse_dates=["Date"], date_format=date_format)
    sse_f = pd.read_csv(f"{base_path}/SSE_{freq}.csv", parse_dates=["Date"], date_format=date_format)

    spy_out_rows = []
    sse_out_rows = []

    for i in range(len(spy_f) - 1):
        start_date = spy_f.loc[i, "Date"]
        end_date = spy_f.loc[i + 1, "Date"] - pd.Timedelta(days=1)
        mask = (spy_d["Date"] >= start_date) & (spy_d["Date"] <= end_date)

        strong_val = spy_f.loc[i, "Strong"]

        # 用 isclose 判断匹配
        if np.isclose(strong_val, spy_f.loc[i, "SPYG"], atol=0.01):
            strong_col = "SPYG"
            weak_col = "SPYV"
        elif np.isclose(strong_val, spy_f.loc[i, "SPYV"], atol=0.01):
            strong_col = "SPYV"
            weak_col = "SPYG"
        else:
            raise ValueError(
                f"SPY 第 {i} 行 Strong 值 {strong_val} 无匹配, SPYG={spy_f.loc[i, 'SPYG']}, SPYV={spy_f.loc[i, 'SPYV']}"
            )

        segment = spy_d.loc[mask].copy()
        segment["Strong"] = segment[strong_col]
        segment["Weak"] = segment[weak_col]
        spy_out_rows.append(segment[["Date", "Strong", "Weak"]])

    for i in range(len(sse_f) - 1):
        start_date = sse_f.loc[i, "Date"]
        end_date = sse_f.loc[i + 1, "Date"] - pd.Timedelta(days=1)
        mask = (sse_d["Date"] >= start_date) & (sse_d["Date"] <= end_date)

        strong_val = sse_f.loc[i, "Strong"]

        if np.isclose(strong_val, sse_f.loc[i, "GPrice"], atol=0.01):
            strong_col = "GPrice"
            weak_col = "VPrice"
        elif np.isclose(strong_val, sse_f.loc[i, "VPrice"], atol=0.01):
            strong_col = "VPrice"
            weak_col = "GPrice"
        else:
            raise ValueError(
                f"SSE 第 {i} 行 Strong 值 {strong_val} 无匹配, GPrice={sse_f.loc[i, 'GPrice']}, VPrice={sse_f.loc[i, 'VPrice']}"
            )

        segment = sse_d.loc[mask].copy()
        segment["Strong"] = segment[strong_col]
        segment["Weak"] = segment[weak_col]
        sse_out_rows.append(segment[["Date", "Strong", "Weak"]])

    # 拼接全部结果并导出
    spy_result = pd.concat(spy_out_rows)
    sse_result = pd.concat(sse_out_rows)

    spy_result.to_csv(f"{base_path}/SPY_{freq}D.csv", index=False)
    sse_result.to_csv(f"{base_path}/SSE_{freq}D.csv", index=False)


