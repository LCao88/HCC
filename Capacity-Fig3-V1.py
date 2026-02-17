import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# --- 设置随机种子和风格 ---
np.random.seed(2024)  # 固定种子以保证每次生成的图都一样漂亮
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']  # PNAS 偏好 Arial


def generate_circles(ax, n_attempts, radius, min_dist_factor, color, bounds=(0, 1, 0, 1), center=None, std_dev=None):
    """
    核心算法：拒绝采样生成圆
    min_dist_factor: 控制重叠程度
       - 2.0 = 完全不重叠 (相切)
       - 1.6 = 轻微重叠 (Uniform)
       - 0.5 = 深度重叠 (Hierarchical)
    """
    circles = []
    min_dist = radius * min_dist_factor

    for _ in range(n_attempts):
        # 如果指定了中心（分层模式），则高斯分布；否则（均匀模式），均匀分布
        if center:
            cx, cy = center
            x = np.random.normal(cx, std_dev)
            y = np.random.normal(cy, std_dev)
        else:
            x = np.random.uniform(bounds[0] + radius, bounds[1] - radius)
            y = np.random.uniform(bounds[2] + radius, bounds[3] - radius)

        # 边界检查
        if not (bounds[0] + radius < x < bounds[1] - radius and bounds[2] + radius < y < bounds[3] - radius):
            continue

        # 碰撞检测 (Check constraints)
        collision = False
        for (px, py) in circles:
            dist = np.sqrt((x - px) ** 2 + (y - py) ** 2)
            if dist < min_dist:  # 距离太近，违反约束
                collision = True
                break

        if not collision:
            circles.append((x, y))
            # 画圆，带有透明度以显示重叠
            circle = patches.Circle((x, y), radius, facecolor=color, edgecolor='white',
                                    linewidth=0.8, alpha=0.6)
            ax.add_patch(circle)

    return len(circles)


# --- 主绘图逻辑 ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300)

# ==========================================
# 左图：Uniform Regime (Light Overlap)
# ==========================================
R_uni = 0.11
# min_dist_factor = 1.5 意味着允许 (2.0 - 1.5) = 0.5R 的重叠深度
# 这就是"一点点overlap"
count_uni = generate_circles(ax1, n_attempts=2000, radius=R_uni, min_dist_factor=1.5,
                             color='#1f77b4', bounds=(0, 1, 0, 1))

ax1.set_title(f"A. Uniform Regime ($K=2$)\nStrict Constraint: Light Overlap Only",
              fontsize=12, fontweight='bold', pad=10)
ax1.text(0.5, 0.05, f"Capacity Reached: {count_uni} Concepts\n(Jamming Limit)",
         ha='center', fontsize=10, fontweight='bold', color='#1f77b4',
         bbox=dict(facecolor='#eef', edgecolor='none', alpha=0.8, boxstyle='round'))

# 画出示例重叠区域（放大镜效果暗示）
# 随便找两个圆画个双向箭头表示距离限制
circle_example = patches.Circle((0.5, 0.5), 0.005, color='black')  # 仅作定位参考，不实际画出

# ==========================================
# 右图：Hierarchical Regime (Deep Overlap)
# ==========================================
R_hier = 0.11
# 定义三个流形中心
centers = [(0.25, 0.7), (0.75, 0.65), (0.4, 0.25)]
colors = ['#d62728', '#2ca02c', '#9467bd']  # 红，绿，紫

total_hier = 0
for idx, center in enumerate(centers):
    # 画流形边界（虚线）
    manifold = patches.Circle(center, 0.28, fill=False, edgecolor='gray', linestyle='--', linewidth=1.5, alpha=0.5)
    ax2.add_patch(manifold)

    # 在流形内生成圆
    # min_dist_factor = 0.6 意味着允许深度重叠，但不能完全重合 (0.6R 的距离)
    # std_dev 控制分布紧凑度
    c = generate_circles(ax2, n_attempts=1000, radius=R_hier, min_dist_factor=0.6,
                         color=colors[idx], bounds=(0, 1, 0, 1), center=center, std_dev=0.08)
    total_hier += c

ax2.set_title(f"B. Hierarchical Regime ($K_{{intra}}=20$)\nRelaxed Constraint: Deep Overlap Allowed",
              fontsize=12, fontweight='bold', pad=10)
ax2.text(0.5, 0.05, f"Capacity Reached: {total_hier} Concepts\n(Manifold Density Gain)",
         ha='center', fontsize=10, fontweight='bold', color='#d62728',
         bbox=dict(facecolor='#fee', edgecolor='none', alpha=0.8, boxstyle='round'))

# --- 公共设置 ---
for ax in [ax1, ax2]:
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    # 画边框
    rect = patches.Rectangle((0.01, 0.01), 0.98, 0.98, linewidth=1.5, edgecolor='#333', facecolor='none')
    ax.add_patch(rect)

plt.tight_layout()
plt.savefig('fig3_packing_corrected.png', bbox_inches='tight')
plt.show()