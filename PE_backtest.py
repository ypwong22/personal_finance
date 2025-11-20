import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calc_anchor(etf='QQQ', years=10):
    df = yf.download(etf, start='1990-01-01')
    df = df['Adj Close'].resample('M').last()

    # 估值数据（用市盈率近似代替）
    val = yf.download(f"^{etf.replace('QQQ','NDX').replace('SPY','GSPC')}", start='1990-01-01')['Adj Close'].resample('M').last()
    # 若无直接P/E数据，可从macrotrends.com或FRED导入，示例用伪造增长率
    epsg = df.pct_change(12*years).rolling(12).mean().fillna(0.05)  # 年化增长假设5%
    ten_year = yf.download("^TNX", start='1990-01-01')['Adj Close'].resample('M').last()/100  # 10年期国债收益率

    # PE模拟序列（仅示意）
    pe = 20 + 10*np.sin(np.linspace(0, len(df)/20, len(df)))  # 可替换为真实历史P/E

    # 指标计算
    pe_med = pd.Series(pe).rolling(12*years).median()
    D_pe = (pe - pe_med)/pe_med
    D_e = (pe/epsg.values)/ten_year.values
    D = 0.4*D_pe + 0.4*D_e/D_e.std()

    out = pd.DataFrame({'Price': df, 'PE': pe, 'D_PE': D_pe, 'D_E': D_e, 'D_Total': D}, index=df.index)

    plt.figure(figsize=(10,5))
    plt.plot(out.index, out['D_Total'], label='脱锚指数')
    plt.axhline(1.5, color='r', linestyle='--')
    plt.title(f"{etf} 脱锚指数（>1.5视为风险区）")
    plt.legend()
    plt.show()

    return out

data = calc_anchor('QQQ')
