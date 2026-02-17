import numpy as np
import matplotlib.pyplot as plt

# --- 风格设置 ---
plt.style.use('default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']


# ==========================================
# 左图 (Panel A): Supply vs. Demand
# ==========================================
def plot_supply_demand(ax):
    # X轴：神经元丢失比例 (0 -> 40%)
    # 我们只关注前 40%，因为后面都是0了
    loss_pct = np.linspace(0, 45, 1000)
    f = loss_pct / 100.0

    # --- 参数设定 ---
    # C_req: 生存所需的认知需求 (归一化为 1.0)
    C_req = 1.0

    # 1. Hierarchical Model (Red)
    # 初始容量极大，衰减极快 (Power Law)
    # alpha = 18, R = 50 (50倍冗余)
    alpha = 18.0
    R_hier = 50.0
    C_supply_hier = R_hier * np.power(1 - f, alpha)

    # 2. Uniform Model (Blue)
    # 初始容量极低 (Theorem 1: Jamming Limit)
    # 假设它只能达到需求的 20% (Deficit)
    R_uni = 0.2
    # 它的衰减比较平缓 (Linear or low alpha)
    C_supply_uni = R_uni * (1 - f)

    # --- 绘图 (Y轴聚焦于 Critical Zone) ---

    # 画需求线 (黑色虚线，正中央)
    ax.axhline(y=C_req, color='black', linestyle=':', linewidth=2, label='Biological Demand ($C_{req}$)')

    # 画 Uniform 线 (蓝色)
    ax.plot(loss_pct, C_supply_uni, color='#1f77b4', linewidth=2.5, linestyle='--',
            label='Uniform Coding\n(Structural Deficit)')

    # 画 Hierarchical 线 (红色)
    # 注意：我们只画出在视图内的部分，或者让它自然延伸出图外
    ax.plot(loss_pct, C_supply_hier, color='#d62728', linewidth=4,
            label='Hierarchical Coding\n(Supply Surplus)')

    # --- 填充区域 ---

    # 1. 绿色区域：有效储备 (Supply > Demand)
    # 这里的上限我们需要截断在视图边缘 (比如 2.0)，以免画出界
    y_fill_top = np.minimum(C_supply_hier, 2.0)
    ax.fill_between(loss_pct, C_req, y_fill_top, where=(C_supply_hier > C_req),
                    color='green', alpha=0.1)

    # 2. 红色区域：功能崩溃 (Supply < Demand)
    # 对于 Hierarchical，这是 Cliff 之后
    # 对于 Uniform，这是全程
    ax.fill_between(loss_pct, 0, C_supply_hier, where=(C_supply_hier <= C_req),
                    color='red', alpha=0.1)

    # --- 关键标注 ---

    # 1. 标注 Hierarchical 的巨大起始点 (Off-chart)
    ax.annotate("Starts at $50 \\times C_{req}$\n(Huge Surplus)",
                xy=(1, 1.9), xytext=(8, 1.6),
                arrowprops=dict(facecolor='#d62728', shrink=0.05),
                color='#d62728', fontweight='bold', fontsize=10)

    # 2. 标注 Uniform 的不足
    ax.text(30, 0.25, "Insufficient Capacity\n($C < C_{req}$)",
            color='#1f77b4', ha='center', fontsize=10, fontweight='bold')

    # 3. 标注 Cliff Edge (交叉点)
    # 计算交叉点
    f_crit = 1.0 - np.power(C_req / R_hier, 1.0 / alpha)
    f_crit_pct = f_crit * 100

    ax.scatter([f_crit_pct], [C_req], color='black', s=100, zorder=10)
    ax.annotate(f"Cliff Edge\n(Reserve Exhausted)",
                xy=(f_crit_pct, C_req), xytext=(f_crit_pct + 12, C_req),
                arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.1", color='black', lw=1.5),
                fontsize=11, fontweight='bold', color='#a00000', va='center')

    # --- 坐标轴调整 ---
    ax.set_ylim(0, 2.0)  # 关键：让 C_req (1.0) 居中
    ax.set_xlim(0, 45)

    # 自定义 Y 轴刻度
    ax.set_yticks([0, 0.2, 1.0, 2.0])
    ax.set_yticklabels(['0', 'Deficit', '$C_{req}$ (Demand)', 'Surplus'])

    ax.set_xlabel('Neuronal Loss ($f$)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Effective Capacity', fontsize=12, fontweight='bold')
    ax.set_title('A. Supply vs. Demand Dynamics', loc='left', fontsize=14, fontweight='bold')

    ax.grid(True, linestyle='--', alpha=0.3)
    # ax.legend(fontsize=9, loc='upper right') # 图例可能会挡住曲线，手动标注更好


# ==========================================
# 右图 (Panel B): Semantic Merging (不变)
# ==========================================
def plot_semantic_merging(ax):
    from scipy.stats import norm
    x = np.linspace(-4, 8, 500)
    y_animal_h = norm.pdf(x, 0, 0.8)
    y_tool_h = norm.pdf(x, 4, 0.8)
    ax.plot(x, y_animal_h, color='#2ca02c', linestyle=':', alpha=0.6)
    ax.plot(x, y_tool_h, color='#ff7f0e', linestyle=':', alpha=0.6)
    y_animal_d = norm.pdf(x, 0, 1.8)
    y_tool_d = norm.pdf(x, 4, 1.8)
    ax.plot(x, y_animal_d, color='#2ca02c', linewidth=2, label='Concept A')
    ax.plot(x, y_tool_d, color='#ff7f0e', linewidth=2, label='Concept B')
    y_overlap = np.minimum(y_animal_d, y_tool_d)
    ax.fill_between(x, 0, y_overlap, color='red', alpha=0.3, hatch='//')
    ax.annotate("Semantic\nMerging", xy=(2, 0.12), xytext=(2, 0.3),
                arrowprops=dict(facecolor='red', arrowstyle='->', lw=2),
                fontsize=10, fontweight='bold', color='red', ha='center')
    ax.set_ylim(0, 0.55)
    ax.set_yticks([])
    ax.set_xticks([0, 4])
    ax.set_xlabel('Semantic Feature Space', fontsize=12, fontweight='bold')
    ax.set_title('B. Loss of Separation ($K_{inter}$)', loc='left', fontsize=14, fontweight='bold')


# --- 主程序 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
plot_supply_demand(ax1)
plot_semantic_merging(ax2)
plt.tight_layout()
plt.savefig('fig4_supply_demand_final.png', dpi=300)
plt.show()