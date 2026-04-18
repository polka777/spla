#!/usr/bin/env python3
"""
mst_profiling.py - Flow Graph для MST алгоритма
"""

import matplotlib.pyplot as plt
import numpy as np

# Данные профилирования (точные названия из вашего вывода)
data = {
    'Load Graph': {
        'time_ms': 44.95,  # 0.044954 sec * 1000
        'description': 'Loading and parsing MTX file'
    },
    'Iteration 1': {
        'Step 1 (min edges for each vertex, gpu)': 20.8342,
        'Step 2 (min edges for each component)': 6.00177,
        'Step 3': 2.13528,
        'Step 4(выбор представителя для каждой компоненты)': 3.86957,
        'Step 5(добавляем найденные ребра в MST)': 1499.29,
        'Step 6(добавляем S)': 833.544,
        'total': 1532.36
    },
    'Iteration 2': {
        'Step 1 (min edges for each vertex, gpu)': 1.958,
        'Step 2 (min edges for each component)': 1.92812,
        'Step 3': 0.956815,
        'Step 4(выбор представителя для каждой компоненты)': 4.13687,
        'Step 5(добавляем найденные ребра в MST)': 303.064,
        'Step 6(добавляем S)': 963.822,
        'total': 312.166
    },
    'Iteration 3': {
        'Step 1 (min edges for each vertex, gpu)': 1.71851,
        'Step 2 (min edges for each component)': 1.97853,
        'Step 3': 0.979112,
        'Step 4(выбор представителя для каждой компоненты)': 3.3038,
        'Step 5(добавляем найденные ребра в MST)': 74.1854,
        'Step 6(добавляем S)': 779.799,
        'total': 82.3
    },
    'Iteration 4': {
        'Step 1 (min edges for each vertex, gpu)': 1.32176,
        'Step 2 (min edges for each component)': 1.86877,
        'Step 3': 0.855121,
        'Step 4(выбор представителя для каждой компоненты)': 2.84357,
        'Step 5(добавляем найденные ребра в MST)': 4.42634,
        'Step 6(добавляем S)': 0,  # нет в последней итерации
        'total': 11.432
    },
    'GPU Total': {
        'time_ms': 4518.66
    },
    'Total': {
        'time_ms': 4940.85
    }
}

# 1. Waterfall Chart (основной Flow Graph)
def plot_waterfall():
    fig, ax = plt.subplots(figsize=(14, 10))
    
    stages = []
    times = []
    colors = []
    
    # Загрузка графа
    stages.append('Load Graph')
    times.append(data['Load Graph']['time_ms'])
    colors.append('#3498db')
    
    # Итерации
    for i in range(1, 5):
        iter_data = data[f'Iteration {i}']
        
        stages.append(f'Iter {i} - Step 5\n(Add to MST)')
        times.append(iter_data['Step 5(добавляем найденные ребра в MST)'])
        colors.append('#e74c3c')
        
        if iter_data['Step 6(добавляем S)'] > 0:
            stages.append(f'Iter {i} - Step 6\n(Update S)')
            times.append(iter_data['Step 6(добавляем S)'])
            colors.append('#e67e22')
    
    # Итого
    stages.append('Total GPU Time')
    times.append(data['GPU Total']['time_ms'])
    colors.append('#9b59b6')
    
    stages.append('Total MST')
    times.append(data['Total']['time_ms'])
    colors.append('#2ecc71')
    
    y_pos = np.arange(len(stages))
    bars = ax.barh(y_pos, times, color=colors)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(stages, fontsize=10)
    ax.set_xlabel('Time (ms)', fontsize=12)
    ax.set_title('MST Algorithm - Flow Graph (Waterfall)', fontsize=14)
    
    # Добавляем значения
    for bar, time in zip(bars, times):
        ax.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, 
                f'{time:.2f} ms', va='center', fontsize=9)
    
    ax.set_xlim(0, max(times) * 1.1)
    plt.tight_layout()
    plt.savefig('mst_waterfall.png', dpi=150)
    plt.show()
    print("✅ Saved: mst_waterfall.png")

# 2. Stacked bar by iteration
def plot_stacked_by_iteration():
    fig, ax = plt.subplots(figsize=(12, 7))
    
    iterations = ['Iteration 1', 'Iteration 2', 'Iteration 3', 'Iteration 4']
    
    # Шаги в порядке выполнения
    steps = ['Step 1 (GPU)', 'Step 2', 'Step 3', 'Step 4', 'Step 5 (Add MST)', 'Step 6 (Update S)']
    
    data_matrix = [
        [20.8342, 6.00177, 2.13528, 3.86957, 1499.29, 833.544],
        [1.958, 1.92812, 0.956815, 4.13687, 303.064, 963.822],
        [1.71851, 1.97853, 0.979112, 3.3038, 74.1854, 779.799],
        [1.32176, 1.86877, 0.855121, 2.84357, 4.42634, 0]
    ]
    
    bottom = np.zeros(len(iterations))
    colors = ['#3498db', '#2ecc71', '#f1c40f', '#e67e22', '#e74c3c', '#9b59b6']
    
    for i, step in enumerate(steps):
        values = [row[i] for row in data_matrix]
        bars = ax.bar(iterations, values, bottom=bottom, label=step, color=colors[i % len(colors)])
        
        # Добавляем значения на столбцы
        for bar, val in zip(bars, values):
            if val > 1:  # показываем только значимые значения
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_y() + bar.get_height()/2,
                       f'{val:.1f}', ha='center', va='center', fontsize=8, color='white')
        bottom += values
    
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('MST Algorithm - Time Distribution by Iteration', fontsize=14)
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('mst_stacked_iteration.png', dpi=150)
    plt.show()
    print("✅ Saved: mst_stacked_iteration.png")

# 3. Pie chart of total time
def plot_total_pie():
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Суммируем время по всем итерациям
    step5_total = (1499.29 + 303.064 + 74.1854 + 4.42634)
    step6_total = (833.544 + 963.822 + 779.799)
    gpu_total = (20.8342 + 1.958 + 1.71851 + 1.32176)
    cpu_steps_total = (6.00177 + 2.13528 + 3.86957 + 
                       1.92812 + 0.956815 + 4.13687 +
                       1.97853 + 0.979112 + 3.3038 +
                       1.86877 + 0.855121 + 2.84357)
    load_total = 44.95
    
    categories = {
        'Step 5 (Add to MST)': step5_total,
        'Step 6 (Update S)': step6_total,
        'Step 1 (GPU)': gpu_total,
        'Steps 2-4 (CPU)': cpu_steps_total,
        'Load Graph': load_total
    }
    
    colors = ['#e74c3c', '#e67e22', '#3498db', '#2ecc71', '#95a5a6']
    wedges, texts, autotexts = ax.pie(
        categories.values(),
        labels=categories.keys(),
        autopct='%1.1f%%',
        colors=colors,
        textprops={'fontsize': 11}
    )
    
    # Выделяем самый большой сектор
    wedges[0].set_edgecolor('white')
    wedges[0].set_linewidth(2)
    
    total_time = sum(categories.values())
    ax.set_title(f'MST Algorithm - Total Time Distribution\n(Total: {total_time:.0f} ms)', fontsize=14)
    plt.tight_layout()
    plt.savefig('mst_total_pie.png', dpi=150)
    plt.show()
    print("✅ Saved: mst_total_pie.png")

# 4. Heatmap
def plot_heatmap():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    iterations = ['Iter 1', 'Iter 2', 'Iter 3', 'Iter 4']
    steps = ['Step 1\n(GPU)', 'Step 2', 'Step 3', 'Step 4', 'Step 5\n(Add MST)', 'Step 6\n(Update S)']
    
    data_matrix = np.array([
        [20.83, 6.00, 2.14, 3.87, 1499.29, 833.54],
        [1.96, 1.93, 0.96, 4.14, 303.06, 963.82],
        [1.72, 1.98, 0.98, 3.30, 74.19, 779.80],
        [1.32, 1.87, 0.86, 2.84, 4.43, 0]
    ])
    
    # Логарифмическая шкала для лучшей визуализации (из-за больших различий)
    im = ax.imshow(np.log1p(data_matrix), cmap='YlOrRd', aspect='auto')
    
    ax.set_xticks(np.arange(len(steps)))
    ax.set_yticks(np.arange(len(iterations)))
    ax.set_xticklabels(steps, fontsize=9)
    ax.set_yticklabels(iterations, fontsize=10)
    
    # Добавляем значения
    for i in range(len(iterations)):
        for j in range(len(steps)):
            val = data_matrix[i, j]
            if val > 0:
                text = ax.text(j, i, f'{val:.1f}',
                              ha="center", va="center", 
                              color="white" if val > 100 else "black", 
                              fontsize=8, fontweight='bold')
    
    ax.set_xlabel('Step', fontsize=12)
    ax.set_ylabel('Iteration', fontsize=12)
    ax.set_title('MST Algorithm - Time Heatmap (ms, log scale)', fontsize=14)
    
    cbar = plt.colorbar(im, label='log(Time + 1) [ms]')
    plt.tight_layout()
    plt.savefig('mst_heatmap.png', dpi=150)
    plt.show()
    print("✅ Saved: mst_heatmap.png")

# 5. Cumulative flow diagram
def plot_cumulative_flow():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    iterations = [1, 2, 3, 4]
    
    # Накопленные значения
    cumulative = {
        'GPU': np.cumsum([20.83, 1.96, 1.72, 1.32]),
        'CPU Steps': np.cumsum([12.01, 7.02, 6.26, 5.57]),
        'Add MST': np.cumsum([1499.29, 303.06, 74.19, 4.43]),
        'Update S': np.cumsum([833.54, 963.82, 779.80, 0])
    }
    
    # Пересчитываем накопленные суммы правильно
    gpu = [20.83, 22.79, 24.51, 25.83]
    cpu = [32.84, 39.86, 46.12, 51.69]
    add_mst = [1532.13, 1835.19, 1909.38, 1913.81]
    update_s = [2365.67, 3329.49, 4109.29, 4109.29]
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#e67e22']
    labels = ['Step 1 (GPU)', 'Steps 2-4 (CPU)', 'Step 5 (Add to MST)', 'Step 6 (Update S)']
    data = [gpu, cpu, add_mst, update_s]
    
    ax.stackplot(iterations, gpu, cpu, add_mst, update_s, 
                 labels=labels, colors=colors, alpha=0.8)
    
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Cumulative Time (ms)', fontsize=12)
    ax.set_title('MST Algorithm - Cumulative Flow Diagram', fontsize=14)
    ax.legend(loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(iterations)
    
    # Добавляем финальное значение
    ax.text(4, 4109, f'Total: 4941 ms', ha='right', va='bottom', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('mst_cumulative.png', dpi=150)
    plt.show()
    print("✅ Saved: mst_cumulative.png")

# 6. Bar chart comparing bottlenecks
def plot_bottlenecks():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    components = ['Step 5\n(Add to MST)', 'Step 6\n(Update S)', 'Step 1 (GPU)', 'Steps 2-4 (CPU)', 'Load Graph']
    times = [1880.96, 2577.16, 25.83, 51.69, 44.95]
    colors = ['#e74c3c', '#e67e22', '#3498db', '#2ecc71', '#95a5a6']
    
    bars = ax.bar(components, times, color=colors)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('MST Algorithm - Main Components Time', fontsize=14)
    
    # Добавляем значения и проценты
    total = sum(times)
    for bar, time in zip(bars, times):
        percentage = (time / total) * 100
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20,
               f'{time:.0f} ms\n({percentage:.1f}%)', 
               ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('mst_bottlenecks.png', dpi=150)
    plt.show()
    print("✅ Saved: mst_bottlenecks.png")

# 7. Iteration time trend
def plot_iteration_trend():
    fig, ax = plt.subplots(figsize=(10, 6))
    
    iterations = [1, 2, 3, 4]
    iter_times = [1532.36, 312.166, 82.3, 11.432]
    
    bars = ax.bar(iterations, iter_times, color='steelblue', edgecolor='black')
    ax.plot(iterations, iter_times, 'ro-', linewidth=2, markersize=8, label='Time per iteration')
    
    ax.set_xlabel('Iteration', fontsize=12)
    ax.set_ylabel('Time (ms)', fontsize=12)
    ax.set_title('MST Algorithm - Time per Iteration (Log Scale)', fontsize=14)
    ax.set_yscale('log')
    ax.set_xticks(iterations)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Добавляем значения
    for bar, time in zip(bars, iter_times):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
               f'{time:.1f} ms', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('mst_iteration_trend.png', dpi=150)
    plt.show()
    print("✅ Saved: mst_iteration_trend.png")

# Запуск всех графиков
if __name__ == "__main__":
    print("=" * 50)
    print("MST Algorithm - Flow Graph Generator")
    print("=" * 50)
    print("\nGenerating visualizations...\n")
    
    plot_waterfall()
    plot_stacked_by_iteration()
    plot_total_pie()
    plot_heatmap()
    plot_cumulative_flow()
    plot_bottlenecks()
    plot_iteration_trend()
    
    print("\n" + "=" * 50)
    print("✅ All graphs generated successfully!")
    print("Files created:")
    print("  - mst_waterfall.png")
    print("  - mst_stacked_iteration.png")
    print("  - mst_total_pie.png")
    print("  - mst_heatmap.png")
    print("  - mst_cumulative.png")
    print("  - mst_bottlenecks.png")
    print("  - mst_iteration_trend.png")
    print("=" * 50)