import numpy as np
import matplotlib.pyplot as plt

# Настройка стиля
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'DejaVu Sans'

# ============================================================
# ГРАФИК 1: RISC-V (столбчатая диаграмма с погрешностями)
# ============================================================
fig1, ax1 = plt.subplots(figsize=(10, 6))

graphs = ['avrora', 'eclipse', 'luindex', 'lusearch', 'sunflow']
values = [2.05, 2.35, 2.25, 2.30, 2.40]
errors = [0.05, 0.05, 0.05, 0.05, 0.05]

x_pos = np.arange(len(graphs))
bars = ax1.bar(x_pos, values, yerr=errors, capsize=8, 
               color='#2E86AB', edgecolor='black', linewidth=1.2,
               error_kw={'linewidth': 1.5})

# Добавляем подписи значений над столбцами
for bar, val in zip(bars, values):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08,
             f'{val:.2f}', ha='center', va='bottom', fontweight='bold')

ax1.set_xticks(x_pos)
ax1.set_xticklabels(graphs, fontsize=13)
ax1.set_xlabel('Графы', fontsize=14, fontweight='bold')
ax1.set_ylabel('Отношение производительности', fontsize=13)
ax1.set_title('RISC-V: Относительная производительность\n(больше = хуже)', 
              fontsize=15, fontweight='bold')
ax1.set_ylim(0, 2.8)
ax1.grid(axis='y', linestyle='--', alpha=0.4)
ax1.set_axisbelow(True)

plt.tight_layout()
plt.savefig('riscv_graph.png', dpi=200, bbox_inches='tight')
plt.show()

# ============================================================
# ГРАФИК 2: x86 (ящик с усами / box plot)
# ============================================================
fig2, ax2 = plt.subplots(figsize=(10, 6))

# Данные в формате [min, q1, median, q3, max]
data = {
    'avrora':   [0.80, 0.90, 1.00, 1.10, 1.25],
    'eclipse':  [1.00, 1.10, 1.20, 1.30, 2.60],
    'luindex':  [0.95, 1.00, 1.05, 1.10, 1.40],
    'lusearch': [0.95, 1.00, 1.08, 1.10, 1.30],
    'sunflow':  [0.95, 1.00, 1.05, 1.10, 1.30]
}

# Преобразуем в список для boxplot
box_data = [data[g] for g in graphs]

# Рисуем boxplot
bp = ax2.boxplot(box_data, labels=graphs, patch_artist=True,
                 showmeans=False, showfliers=True,
                 whiskerprops={'linewidth': 1.5},
                 capprops={'linewidth': 1.5},
                 medianprops={'linewidth': 2, 'color': 'darkred'})

# Раскрашиваем ящики
colors = ['#A23B72', '#F18F01', '#2E86AB', '#73AB84', '#C73E1D']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.75)
    patch.set_edgecolor('black')
    patch.set_linewidth(1.5)

# Добавляем горизонтальную линию на y=1.0 (baseline)
ax2.axhline(y=1.0, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax2.text(len(graphs)-0.3, 1.02, 'baseline = 1.0', fontsize=10, color='gray')

ax2.set_xlabel('Графы', fontsize=14, fontweight='bold')
ax2.set_ylabel('Отношение производительности', fontsize=13)
ax2.set_title('x86: Распределение значений\n(Min, Q1, Медиана, Q3, Max)', 
              fontsize=15, fontweight='bold')
ax2.grid(axis='y', linestyle='--', alpha=0.4)
ax2.set_axisbelow(True)

plt.tight_layout()
plt.savefig('x86_graph.png', dpi=200, bbox_inches='tight')
plt.show()