import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# --- 风格设置 ---
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']


def add_fancy_box(ax, xy, width, height, text, color, subtext=None, alpha=0.9):
    """画圆角矩形"""
    box = patches.FancyBboxPatch(xy, width, height, boxstyle="round,pad=0.04",
                                 ec=color, fc='white', lw=1.5, alpha=alpha)
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height * 0.6, text, ha='center', va='center',
            fontsize=9, fontweight='bold', color=color)
    if subtext:
        ax.text(xy[0] + width / 2, xy[1] + height * 0.25, subtext, ha='center', va='center',
                fontsize=7, color='gray')


# --- Panel A: Anatomy (Trisynaptic Loop 修正版) ---
def plot_anatomy(ax):
    ax.set_title("A. Biological Architecture (EC-HC Loop)", loc='left', fontsize=12, fontweight='bold')

    # 1. EC (Entorhinal Cortex) - 左侧大本营
    add_fancy_box(ax, (0.02, 0.3), 0.22, 0.4, "Entorhinal\nCortex (EC)", "#1f77b4", "Input/Output\nHub")

    # 2. DG (Dentate Gyrus) - 上方
    add_fancy_box(ax, (0.35, 0.65), 0.22, 0.25, "DG", "#d62728", "Pattern\nSeparation")

    # 3. CA3 - 右侧
    add_fancy_box(ax, (0.7, 0.4), 0.22, 0.25, "CA3", "#2ca02c", "Pattern\nCompletion")

    # 4. CA1 - 下方
    add_fancy_box(ax, (0.35, 0.1), 0.22, 0.25, "CA1", "#9467bd", "Integration")

    # --- 连接线 (The Loop) ---

    # Input -> EC
    ax.annotate("Cortex", xy=(0.02, 0.5), xytext=(-0.12, 0.5),
                arrowprops=dict(arrowstyle="->", color='black', lw=2), fontsize=9, ha='center')

    # EC -> DG (Perforant Path)
    ax.annotate("", xy=(0.35, 0.77), xytext=(0.24, 0.65),
                arrowprops=dict(arrowstyle="->", color='gray', lw=1.5, connectionstyle="arc3,rad=-0.2"))

    # DG -> CA3 (Mossy Fibers)
    ax.annotate("", xy=(0.7, 0.55), xytext=(0.57, 0.77),
                arrowprops=dict(arrowstyle="->", color='gray', lw=1.5, connectionstyle="arc3,rad=-0.2"))

    # CA3 -> CA1 (Schaffer Collaterals)
    ax.annotate("", xy=(0.57, 0.22), xytext=(0.81, 0.4),
                arrowprops=dict(arrowstyle="->", color='gray', lw=1.5, connectionstyle="arc3,rad=-0.2"))

    # CA1 -> EC (Feedback / Subiculum) - 关键反馈回路！
    ax.annotate("", xy=(0.24, 0.35), xytext=(0.35, 0.22),
                arrowprops=dict(arrowstyle="->", color='black', lw=1.5, linestyle='--',
                                connectionstyle="arc3,rad=-0.2"))
    ax.text(0.3, 0.28, "Feedback", fontsize=7, rotation=30)

    # 标注功能
    # DG附近
    ax.text(0.46, 0.62, "$K_{inter}$", color='#d62728', fontsize=8, fontweight='bold')
    # CA3附近
    ax.text(0.81, 0.35, "$K_{intra}$", color='#2ca02c', fontsize=8, fontweight='bold')

    ax.set_xlim(-0.15, 1.0)
    ax.set_ylim(0.05, 0.95)
    ax.axis('off')


# --- Panel B & C (保持不变) ---
def plot_geometry(ax):
    ax.set_title("B. Partitioned State Space", loc='left', fontsize=12, fontweight='bold')
    large_circle = patches.Circle((0.5, 0.5), 0.45, ec='black', fc='#f9f9f9', lw=2)
    ax.add_patch(large_circle)
    ax.text(0.5, 0.96, "Neural Space ($N$)", ha='center', fontsize=10, fontweight='bold')
    radius = 0.22
    centers = [(0.35, 0.6), (0.65, 0.6), (0.5, 0.3)]
    colors = ['#aec7e8', '#ffbb78', '#98df8a']
    for i, (cx, cy) in enumerate(centers):
        sub_circle = patches.Circle((cx, cy), radius, ec='gray', fc=colors[i], lw=1.5, linestyle='--', alpha=0.5)
        ax.add_patch(sub_circle)
        ax.text(cx, cy, f"$N_{{loc}}^{{{i + 1}}}$", ha='center', va='center', fontsize=11, fontweight='bold')
    ax.annotate("Slight Overlap\n($K_{inter} > 0$)", xy=(0.5, 0.6), xytext=(0.5, 0.8),
                arrowprops=dict(arrowstyle="->", color='black', lw=1), fontsize=9, ha='center')
    ax.text(0.5, 0.05, "Nearly Orthogonal Subspaces", ha='center', fontsize=9, color='gray')
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)


def plot_constraints(ax):
    ax.set_title("C. The $K_{inter} \ll K_{intra}$ Constraint", loc='left', fontsize=12, fontweight='bold')
    c1_center = (0.3, 0.5)
    c2_center = (0.7, 0.5)
    m_radius = 0.22
    c1 = patches.Circle(c1_center, m_radius, ec='gray', fc='#f0f0f0', lw=1.5, linestyle='--', alpha=0.7)
    ax.add_patch(c1)
    ax.text(0.3, 0.8, "Manifold A", color='gray', ha='center', fontsize=9, fontweight='bold')
    c2 = patches.Circle(c2_center, m_radius, ec='gray', fc='#f0f0f0', lw=1.5, linestyle='--', alpha=0.7)
    ax.add_patch(c2)
    ax.text(0.7, 0.8, "Manifold B", color='gray', ha='center', fontsize=9, fontweight='bold')
    ax.annotate("", xy=(0.5, 0.5), xytext=(0.5, 0.65),
                arrowprops=dict(arrowstyle="->", color='gray', lw=1), fontsize=8)
    ax.text(0.5, 0.67, "Manifold Overlap\n($K_{inter} > 0$)", ha='center', fontsize=8, color='gray')
    c_radius = 0.11
    concepts_a = [(0.24, 0.55), (0.36, 0.55), (0.3, 0.42)]
    for (cx, cy) in concepts_a:
        circle = patches.Circle((cx, cy), c_radius, fc='#1f77b4', ec='white', alpha=0.7)
        ax.add_patch(circle)
    ax.text(0.3, 0.5, "$K_{intra}$\nVery High", ha='center', va='center', fontsize=9, color='white', fontweight='bold',
            zorder=10)
    concepts_b = [(0.64, 0.55), (0.76, 0.55), (0.7, 0.42)]
    for (cx, cy) in concepts_b:
        circle = patches.Circle((cx, cy), c_radius, fc='#d62728', ec='white', alpha=0.7)
        ax.add_patch(circle)
    ax.annotate("", xy=(0.38, 0.55), xytext=(0.62, 0.55),
                arrowprops=dict(arrowstyle="|-|", color='black', lw=1.5, linestyle='-'))
    ax.text(0.5, 0.53, "Minimal Concept Overlap", ha='center', fontsize=8, color='black', fontweight='bold', zorder=10)
    ax.text(0.3, 0.22, "Deep Dense Packing\n(Allowed)", ha='center', fontsize=9, color='#1f77b4')
    ax.text(0.7, 0.22, "Deep Dense Packing\n(Allowed)", ha='center', fontsize=9, color='#d62728')
    ax.axis('off')
    ax.set_xlim(0, 1)
    ax.set_ylim(0.15, 0.9)


# --- 主程序 ---
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5), dpi=300)
plot_anatomy(ax1)
plot_geometry(ax2)
plot_constraints(ax3)
plt.tight_layout()
plt.savefig('fig1_anatomy_final.png', dpi=300)
plt.show()