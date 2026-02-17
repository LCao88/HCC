import numpy as np
import matplotlib.pyplot as plt

# --- 1. 参数调优 (Fine-tuning) ---
# 范围: 10^2 到 10^7
N = np.logspace(2.0, 7.0, 1000)

# 关键参数调整
M = 40  # 概念稀疏度
N_loc = 8000  # 局部模组大小 (推迟交叉点的关键：只有 N > 8000 才有资格谈分层)

# 斜率控制
K_uniform = 3.5  # 蓝线斜率 (4.5): 让它在初期增长得非常快，压制红线
K_inter = 2  # 红线基础斜率 (3): 比较慢
K_intra = 25  # 红线后期的爆发红利


# --- 2. 核心公式 ---

def calculate_uniform_capacity(n_array, m, k):
    """
    均匀分布 (Blue): 初期猛涨，后期撞墙
    """
    # 基础容量
    log_c = (k + 1) * (np.log10(n_array) - np.log10(m))

    # 拥堵饱和 (Soft Saturation)
    # 调整 saturation_start 到 4.5 (约 30,000)，让它在该处开始变平
    saturation_start = 4.5
    # 惩罚力度加大，模拟“维度灾难”的不可逾越性
    penalty = 2.5 * np.log10(1 + np.exp(3.0 * (np.log10(n_array) - saturation_start)))

    return log_c - penalty


def calculate_hierarchical_capacity(n_array, n_loc, m, k_inter, k_intra):
    """
    分层结构 (Red): 初期有沉重负担，后期线性增长
    """
    # 1. 全局寻址
    log_G = (k_inter + 1) * (np.log10(n_array) - np.log10(n_loc))

    # 2. 局部红利 (Local Gain)
    max_local_gain = (k_intra + 1) * (np.log10(n_loc) - np.log10(m))

    # 3. 结构成熟度 (Sigmoid Switch)
    # 只有当 N 接近 N_loc 时，红利才开始释放
    # steepness=5 让开关更陡峭
    center = np.log10(n_loc)
    maturity = 1 / (1 + np.exp(-5 * (np.log10(n_array) - center)))

    # 4. 基础设施税 (Infrastructure Tax) - 关键调整！
    # 在 N < N_loc 时，强制扣除容量，模拟分层的低效
    # 这个 tax 会随着 N 增大而消失
    tax = 5.0 * (1 - maturity)

    total_log_C = log_G + (max_local_gain * maturity) - tax

    return total_log_C


# 计算
y_uniform = calculate_uniform_capacity(N, M, K_uniform)
y_hierarchical = calculate_hierarchical_capacity(N, N_loc, M, K_inter, K_intra)

# 找交叉点
diff = y_hierarchical - y_uniform
try:
    cross_idx = np.where(diff > 0)[0][0]
    cross_x = N[cross_idx]
    cross_y = y_uniform[cross_idx]
    print(f"✅ 成功！交叉点发生在 N = {cross_x:.0f} (10^{np.log10(cross_x):.2f})")
except:
    print("❌ 未找到交叉点，请检查参数范围")
    cross_x, cross_y = 10 ** 4, 10

# --- 3. 绘图 (PNAS Style) ---

fig, ax = plt.subplots(figsize=(10, 7))
# 使用无衬线字体模拟 PNAS 风格 (Arial/Helvetica)
plt.rcParams['font.family'] = 'sans-serif'

# 绘图
ax.plot(N, y_uniform, label='Uniform Random Coding ($K=3.5$)\n(Optimal for small networks)',
        color='#0072B2', linewidth=3, linestyle='--')
ax.plot(N, y_hierarchical, label='Hierarchical Coding ($K_{inter}=2, K_{intra}=25$)\n(Optimal for large networks)',
        color='#D55E00', linewidth=3)

# 标记交叉点
ax.scatter([cross_x], [cross_y], color='black', s=150, zorder=10)

# 动态标注
offset_x = cross_x * 0.4  # 文字放左边一点
offset_y = cross_y + 8
ax.annotate(f'$N_c \\approx 10^{{{np.log10(cross_x):.1f}}}$\n(Phase Transition)',
            xy=(cross_x, cross_y), xytext=(offset_x, offset_y),
            arrowprops=dict(facecolor='black', arrowstyle='->', linewidth=2),
            fontsize=14, fontweight='bold', ha='center')

# 区域填充
ax.fill_between(N, y_uniform, y_hierarchical, where=(N > cross_x),
                color='#D55E00', alpha=0.1)
ax.text(10 ** 6, cross_y - 10, "Manifold\nGain", color='#D55E00', fontsize=14, fontweight='bold', ha='center')

# 坐标轴美化
ax.set_xscale('log')
ax.set_xlabel('Total Neural Population ($N$)', fontsize=16, fontweight='bold')
ax.set_ylabel('Memory Capacity ($\ln C$)', fontsize=16, fontweight='bold')
ax.set_title('Topological Phase Transition of Memory Capacity', fontsize=18, pad=20, fontweight='bold')

# 细节调整
ax.grid(True, which="major", ls="-", alpha=0.2)
ax.legend(fontsize=12, loc='upper left', framealpha=0.95)
ax.set_xlim(10 ** 2, 10 ** 7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('fig2_phase_transition_final.png', dpi=300)
plt.show()