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
    计算短线与长线的税后收益比较，绘制不同短线收益率情况下的图
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


def compare_tax_strategies_grid(
    t_short=0.24,      # 短期资本利得税率
    t_long=0.15,       # 长期资本利得税率
    g_long=0.20,       # 长期平均年化收益
):
    """
    计算税后收益和长线打平所需要的短线收益率乘数，绘制不同交易频率和持有年数下的图。
    """

    k_list = np.arange(2, 25, 4)
    N_list = np.arange(1, 10, 1)

    short_to_long_ratio = np.full([len(k_list), len(N_list)], np.nan)

    for i,k in enumerate(k_list):
        # 长线复利：持有 N 年后一次纳税
        # long_after_tax_factor = 1 + (1 - t_long) * ((1 + g_long) ** N - 1)
        # 短线复利：每次交易后立即纳税
        # short_after_tax_factor = (1 + r_short / k * (1 - t_short)) ** (k * N)
        r_short = ((1 + (1 - t_long) * ((1 + g_long) ** N_list - 1))**(1/(k * N_list)) - 1) * k / (1-t_short)
        short_to_long_ratio[i,:] = r_short #  / g_long

    plt.figure(figsize=(8, 5))
    cf = plt.imshow(short_to_long_ratio, cmap = 'viridis')

    plt.colorbar(cf)
    plt.xticks(range(len(N_list)))
    plt.gca().set_xticklabels(N_list)
    plt.yticks(range(len(k_list)))
    plt.gca().set_yticklabels(k_list)

    plt.xlabel('持有年数')
    plt.ylabel('短线每年交易次数')
    plt.title(f'短线收益率 (长线收益率={g_long}, 短线税率={t_short}, 长线税率={t_long})')
    plt.grid(True)
    plt.show()

# 所有输入参数皆为运行假设
#compare_tax_strategies(
#    t_short=0.24,  # 短期税率
#    t_long=0.15,   # 长期税率
#    k=12,          # 年内交易次数
#    g_long=0.20,   # 长线年化
#    N=3            # 总持有年数
#)

compare_tax_strategies_grid()
