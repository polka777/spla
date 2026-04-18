import matplotlib.pyplot as plt
import numpy as np

tests = ['can_1054', 'dwt_1007', 'dwt_1242', 'dwt_2680', 'epb0', 
         'G41', 'gre_1107', 'Journals', 'MISKnowledgeMap', 'USAir97']

spla_powervr = [724.77, 624.98, 968.26, 6046.70, 3412.83, 2585.46, 1857.86, 43.01, 7649.09, 210.78]
spla_amd = [703.63, 638.36, 930.58, 6215.28, 3420.49, 2508.39, 1851.37, 33.21, 7663.68, 180.31]
spla_cpu = [951.85, 1351.75, 1592.24, 9394.40, 3904.07, 4905.49, 2127.43, 36.79, 10365.82, 182.17]

x = np.arange(len(tests))
width = 0.25

fig, ax = plt.subplots(figsize=(14, 7))
bars1 = ax.bar(x - width, spla_powervr, width, label='PowerVR BXE-2-32', color='#1f77b4')
bars2 = ax.bar(x, spla_amd, width, label='AMD CAICOS', color='#ff7f0e')
bars3 = ax.bar(x + width, spla_cpu, width, label='CPU Spacemit X60', color='#2ca02c')

ax.set_yscale('log')
ax.set_ylabel('Время выполнения, мс', fontsize=12)
ax.set_xlabel('Граф', fontsize=12)
ax.set_title('Сравнение производительности Spla на трёх платформах', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(tests, rotation=45, ha='right')
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3, which='both', linestyle='--', linewidth=0.5)

# Добавление значений над столбцами (опционально, только для маленьких значений)
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                f'{height:.0f}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# Вывод минимальных и максимальных значений
print(f"\nЛучшее время на PowerVR: {min(spla_powervr):.2f} мс (тест {tests[np.argmin(spla_powervr)]})")
print(f"Худшее время на PowerVR: {max(spla_powervr):.2f} мс (тест {tests[np.argmax(spla_powervr)]})")
print(f"\nЛучшее время на AMD: {min(spla_amd):.2f} мс (тест {tests[np.argmin(spla_amd)]})")
print(f"Худшее время на AMD: {max(spla_amd):.2f} мс (тест {tests[np.argmax(spla_amd)]})")
print(f"\nЛучшее время на CPU: {min(spla_cpu):.2f} мс (тест {tests[np.argmin(spla_cpu)]})")
print(f"Худшее время на CPU: {max(spla_cpu):.2f} мс (тест {tests[np.argmax(spla_cpu)]})")