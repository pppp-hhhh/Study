import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义常量
V = 10800  # 车间容积，单位：m³
Q = 1500   # 通风量，单位：m³/min
c0_in = 0.04 / 100  # 输入空气中CO2浓度：0.04%
c_initial = 0.12 / 100  # 初始CO2浓度：0.12%

print("问题分析：")
print(f"车间容积 V = {V} m³")
print(f"通风量 Q = {Q} m³/min")
print(f"输入空气中CO2浓度 c0_in = {c0_in*100:.2f}%")
print(f"初始CO2浓度 c_initial = {c_initial*100:.2f}%")

# 问题(1)：建立CO2含量变化的微分方程
print("\n问题(1)：建立车间CO2含量所遵循的规律")

# 设t时刻车间内CO2浓度为c(t)
t = sp.symbols('t')
c = sp.Function('c')  # 先定义函数c


# 微分方程建立：
# CO2量的变化率 = 输入的CO2速率 - 输出的CO2速率
# dc/dt * V = Q * c0_in - Q * c(t)
# 所以：dc/dt = (Q/V) * (c0_in - c(t))

# 使用sympy建立微分方程
diff_eq = sp.Eq(sp.diff(c(t), t), (Q/V) * (c0_in - c(t)))

print("\n微分方程：")
print(diff_eq)

# 现在将第一个任务标记为完成，开始第二个任务
# 求解微分方程
sol = sp.dsolve(diff_eq, c(t))

print("\n微分方程的通解：")
print(sol)

# 应用初始条件 t=0 时，c(0) = c_initial
C1 = sp.symbols('C1')  # 通解中的常数
initial_condition = sol.subs(t, 0).subs(c(0), c_initial)
C1_value = sp.solve(initial_condition, C1)[0]

print(f"\n代入初始条件求得常数 C1 = {C1_value}")

# 特解
specific_sol = sol.subs(C1, C1_value)

print("\n满足初始条件的特解：")
print(specific_sol)

# 简化特解
simplified_sol = sp.simplify(specific_sol.rhs)

print("\n简化后的特解：")
print(f"c(t) = {simplified_sol}")

# 计算Q/V的值
rate = Q / V
print(f"\n通风率 Q/V = {rate:.6f} per minute")

# 将符号解转换为数值函数
sol_func = sp.lambdify(t, simplified_sol, 'numpy')

# 问题(2)：计算10分钟后的CO2百分比
t10 = 10
c10 = sol_func(t10)

print(f"\n问题(2)：鼓风机开动10分钟后")
print(f"10分钟后CO2浓度：{c10*100:.4f}%")

# 计算CO2浓度随时间的变化
# 创建时间数组
times = np.linspace(0, 30, 300)  # 0到30分钟，300个点
concentrations = sol_func(times)

# 计算最终稳定浓度（当t→∞时）
c_inf = c0_in  # 最终将趋近于输入浓度
print(f"\n当t→∞时，CO2浓度趋近于输入浓度：{c_inf*100:.2f}%")

# 计算达到接近稳定状态所需的时间（例如，达到0.05%）
threshold = 0.05 / 100
for i, c_val in enumerate(concentrations):
    if abs(c_val - c_inf) < 0.0001:  # 当差距小于0.01%
        print(f"大约在 t = {times[i]:.2f} 分钟后，CO2浓度接近稳定状态")
        break

# 创建可视化
plt.figure(figsize=(10, 6))

# 绘制CO2浓度随时间的变化
plt.plot(times, concentrations * 100, 'b-', linewidth=2, label='CO2浓度')

# 标记初始浓度和输入浓度
plt.axhline(y=c_initial*100, color='r', linestyle='--', label=f'初始浓度: {c_initial*100:.2f}%')
plt.axhline(y=c0_in*100, color='g', linestyle='--', label=f'输入浓度: {c0_in*100:.2f}%')

# 标记10分钟时的浓度
plt.plot(t10, c10*100, 'ro', markersize=8, label=f'10分钟时: {c10*100:.4f}%')
plt.axvline(x=t10, color='orange', linestyle=':', alpha=0.7)

# 添加标签和标题
plt.title('车间CO2浓度随时间的变化', fontsize=14)
plt.xlabel('时间 (分钟)', fontsize=12)
plt.ylabel('CO2浓度 (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10)

# 添加数学公式
formula_text = f'c(t) = {c0_in*100:.2f}% + ({c_initial*100:.2f}% - {c0_in*100:.2f}%) * e^(-{rate:.6f}t)'
plt.figtext(0.5, 0.01, formula_text, ha='center', fontsize=10)

# 调整布局
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

print("\n可视化图表已创建，运行脚本即可查看。")

# 显示图表
plt.show()