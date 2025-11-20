"""Test the strategy of an improved DCA - buying all accumulated dollars only
   when the price dips below 50-day moving average. Based on NASDAQ.
"""
import pandas as pd

# 读取你的Excel（假设第一列是日期，第二列是Close价格）
df = pd.read_excel('qqq_daily_all.xlsx', index_col=0, parse_dates=True)
df = df.sort_index()
df = df[['Price']].copy()          # 如果你的列名不是Close，改成对应的名字
df.columns = ['price']

# 只测熊市 —— 结果仍然是DCA最优
# df = df.loc[df.index.year <= 2008, :]

def backtest(ma_period=None, ma_type='SMA', monthly_invest=1000):
    cash = 0.0
    shares = 0.0
    total_invested = 0.0
    
    # 计算日线均线
    if ma_period is not None:
        if ma_type == 'EMA':
            df['ma'] = df['price'].ewm(span=ma_period, adjust=False).mean()
        else:  # SMA
            df['ma'] = df['price'].rolling(ma_period).mean()
    
    # 关键：转成每月最后一个交易日的数据
    monthly_df = df.resample('ME').last()
    
    for date, row in monthly_df.iterrows():
        # 1. 每月先发工资（攒现金）
        cash += monthly_invest
        total_invested += monthly_invest
        
        price_today = row['price']
        
        if ma_period is None:                     # 普通DCA：每月都买
            shares += cash / price_today
            cash = 0
        else:                                      # 策略：只有月末价格 < 均线才全砸
            ma_today = row['ma']
            if pd.notna(ma_today) and price_today < ma_today:
                shares += cash / price_today       # 攒的所有钱一次性买入
                cash = 0
            # 否则继续攒钱，不买

        # print(cash) # debug

    # 计算最终结果
    final_price = df['price'].iloc[-1]
    final_value = shares * final_price + cash
    years = (df.index[-1] - df.index[0]).days / 365.25
    cagr = (final_value / total_invested) ** (1/years) - 1

    print(f"总投入: {total_invested/1000:.1f}k$")
    print(f"总持股: {shares}")
    print(f"最终市值: {final_value/1000:.2f}k$")
    print(f"年化收益率: {cagr*100:.2f}%\n")

print("=== 普通每月DCA ===")
backtest(None)

print("=== 30日SMA策略 ===")
backtest(30, 'SMA')

print("=== 50日EMA策略 ===")
backtest(50, 'EMA')