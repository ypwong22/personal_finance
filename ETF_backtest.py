# 📦 导入必要库
import yfinance as yf
import pandas as pd
import numpy as np

# ===== 用户设置区 =====
start_date = "2022-01-01"
end_date = "2022-10-01"

# S&P500 11大板块 + 国防主题ETF
etfs = {
    "XLK": "信息科技",
    "XLC": "通信服务",
    "XLY": "可选消费",
    "XLP": "必需消费",
    "XLV": "医疗保健",
    "XLE": "能源",
    "XLI": "工业",
    "XLU": "公用事业",
    "XLF": "金融",
    "XLRE": "房地产",
    "XAR": "国防与航空"
}

# ===== 主程序 =====
results = []

for symbol, name in etfs.items():
    data = yf.download(symbol, start=start_date, end=end_date)["Adj Close"]
    if len(data) == 0:
        continue

    # 最大回撤
    roll_max = data.cummax()
    drawdown = (data - roll_max) / roll_max
    max_dd = drawdown.min() * 100

    # 从最低点反弹收益
    min_index = data.idxmin()
    rebound = ((data[-1] / data[min_index]) - 1) * 100

    results.append({
        "ETF": symbol,
        "板块": name,
        "最大回撤(%)": round(max_dd, 1),
        "回稳期收益(%)": round(rebound, 1)
    })

df = pd.DataFrame(results).sort_values("最大回撤(%)")
print(df.to_string(index=False))

# ===== 可选：保存结果 =====
# df.to_csv("SP500_sector_drawdown_analysis.csv", index=False)
