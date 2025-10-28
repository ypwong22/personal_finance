import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# 尝试设置中文字体（不同系统取不同字体）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Heiti TC', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 避免负号显示为方块

def compare_tax_strategies(
    t_short=0.24,      # 短期资本利得税率
    t_long=0.15,       # 长期资本利得税率
    k=12,              # 每年短线交易次数
    g_long=0.20,       # 长期平均年化收益
    N=3                # 总年数
):
    """
    计算短线与长线的税后收益比较，并绘图
    """

    # 长线复利：持有 N 年后一次纳税
    long_after_tax_factor = 1 + (1 - t_long) * ((1 + g_long) ** N - 1)

    # 短线复利：每次交易后立即纳税
    # 测试不同的短线 annualized 收益率
    r_short = np.linspace(0.5, 1.5, 100) * g_long
    short_after_tax_factor = (1 + r_short / k * (1 - t_short)) ** (k * N)

    plt.figure(figsize=(8, 5))
    plt.plot(r_short, short_after_tax_factor, color='r', label='短线税后倍数')
    plt.axhline(long_after_tax_factor, color='b', linestyle='-', label='长线税后倍数')
    plt.axvline(g_long, color='k', linestyle='--', label='长线交易年化收益率 (%)')
    plt.xlabel('短线交易年化收益率 (%)')
    plt.ylabel('税后增长倍数')
    plt.title(f'短线 vs 长线 ({N}年, 每年{k}次交易)')
    plt.legend()
    plt.grid(True)
    plt.show()

# 所有输入参数皆为运行假设
compare_tax_strategies(
    t_short=0.24,  # 短期税率
    t_long=0.15,   # 长期税率
    k=12,          # 年内交易次数
    g_long=0.20,   # 长线年化
    N=3            # 总持有年数
)
