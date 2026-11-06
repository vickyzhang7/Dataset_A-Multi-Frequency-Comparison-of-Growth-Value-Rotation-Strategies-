import pandas as pd
import os

# 设置基础路径和频率列表
base_path = "/Users/xiaohuidexiaojiaoqi/Desktop"
frequencies = ["W", "M", "Q", "H", "A"]

# 读取日度数据（含日期列和对应指标列）
spy_d = pd.read_csv(f"{base_path}/SPY_D.csv", parse_dates=["Date"])
sse_d = pd.read_csv(f"{base_path}/SSE_VG.csv", parse_dates=["Date"])

for freq in frequencies:
    print(f"处理频率：{freq}...")

    # 读取频率文件
    spy_f = pd.read_csv(f"{base_path}/SPY_{freq}.csv", parse_dates=["Date"])
    sse_f = pd.read_csv(f"{base_path}/SSE_{freq}.csv", parse_dates=["Date"])

    spy_out_rows = []
    sse_out_rows = []

    # ---------- SPY 数据处理 ----------
    for i in range(1, len(spy_f)):
        start_date = spy_f.loc[i - 1, "Date"]
        end_date = spy_f.loc[i, "Date"]

        strong_val = spy_f.loc[i, "Strong"]
        spyg_val = spy_f.loc[i, "SPYG"]
        spyv_val = spy_f.loc[i, "SPYV"]

        if strong_val == spyg_val:
            strong_col = "SPYG"
            weak_col = "SPYV"
        elif strong_val == spyv_val:
            strong_col = "SPYV"
            weak_col = "SPYG"
        else:
            raise ValueError(f"SPY 第{i}行 Strong值 {strong_val} 无匹配 SPYG({spyg_val}) 或 SPYV({spyv_val})")

        mask = (spy_d["Date"] >= start_date) & (spy_d["Date"] <= end_date)
        segment = spy_d.loc[mask].copy()
        segment["Strong"] = segment[strong_col]
        segment["Weak"] = segment[weak_col]
        spy_out_rows.append(segment[["Date", "Strong", "Weak"]])

    # ---------- SSE 数据处理 ----------
    for i in range(1, len(sse_f)):
        start_date = sse_f.loc[i - 1, "Date"]
        end_date = sse_f.loc[i, "Date"]

        strong_val = sse_f.loc[i, "Strong"]
        g_val = sse_f.loc[i, "GPrice"]
        v_val = sse_f.loc[i, "VPrice"]

        if strong_val == g_val:
            strong_col = "GPrice"
            weak_col = "VPrice"
        elif strong_val == v_val:
            strong_col = "VPrice"
            weak_col = "GPrice"
        else:
            raise ValueError(f"SSE 第{i}行 Strong值 {strong_val} 无匹配 GPrice({g_val}) 或 VPrice({v_val})")

        mask = (sse_d["Date"] >= start_date) & (sse_d["Date"] <= end_date)
        segment = sse_d.loc[mask].copy()
        segment["Strong"] = segment[strong_col]
        segment["Weak"] = segment[weak_col]
        sse_out_rows.append(segment[["Date", "Strong", "Weak"]])

    # 合并并输出文件
    spy_result = pd.concat(spy_out_rows)
    sse_result = pd.concat(sse_out_rows)

    spy_result.to_csv(f"{base_path}/SPY_{freq}D.csv", index=False)
    sse_result.to_csv(f"{base_path}/SSE_{freq}D.csv", index=False)

print("✅ 所有频率处理完成。")
