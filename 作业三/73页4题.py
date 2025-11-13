import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# 定义时间t
t = sp.symbols('t')
# p是鲑鱼t时刻的总数，d是鲨鱼猎杀鲑鱼的速率
p = sp.Function('p')(t)
d = sp.Function('d')(t)

# 假设鲑鱼的自然增长率为r
r = 0.01  # 这里使用0.01作为示例，可根据实际题目调整

# 鲨鱼猎杀速率的微分方程: sp.diff(d,t) = 0.003*p
d_equation = sp.Eq(sp.diff(d,t), 0.003*p)

# 修正后的鲑鱼总数增长率微分方程
true_speed_p_equation = sp.Eq(sp.diff(p,t), r*p - d - 0.002)

print("鲨鱼猎杀速率方程:", d_equation)
print("鲑鱼总数增长率方程:", true_speed_p_equation)

# 初始条件
initial_p = 1000000  # t=0时鲑鱼数量
initial_d = 0.001*(initial_p)**2  # t=0时鲨鱼猎杀速率

print(f"初始条件: t=0时，p(0)={initial_p}, d(0)={initial_d}")

# 定义微分方程组用于数值求解
def system(y, t, r):
    p, d = y
    dpdt = r*p - d - 0.002
    dddt = 0.003*p
    return [dpdt, dddt]

# 时间点
# 短期分析（前100分钟）
t_short = np.linspace(0, 100, 1000)
# 长期分析（前1000分钟）
t_long = np.linspace(0, 1000, 1000)

# 求解微分方程组
# 使用不同的r值进行敏感性分析
r_values = [0.005, 0.01, 0.02]
results = {}

for r_val in r_values:
    # 求解短期行为
    sol_short = odeint(system, [initial_p, initial_d], t_short, args=(r_val,))
    # 求解长期行为
    sol_long = odeint(system, [initial_p, initial_d], t_long, args=(r_val,))
    results[r_val] = {'short': sol_short, 'long': sol_long}

print("\n微分方程组数值求解完成。")
print("\n长期行为(t→∞)分析：")
for r_val in r_values:
    # 获取长期解的最终值
    final_p = results[r_val]['long'][-1, 0]
    final_d = results[r_val]['long'][-1, 1]
    
    print(f"\n当r = {r_val}时:")
    if final_p < 1000:  # 假设低于1000视为灭绝
        print(f"  鲑鱼数量最终趋近于灭绝 ({final_p:.2f})")
    elif final_p > initial_p * 1.5:  # 增长超过50%
        print(f"  鲑鱼数量持续增长，最终值: {final_p:.2f}")
    else:
        print(f"  鲑鱼数量趋于稳定，最终值: {final_p:.2f}")
    print(f"  鲨鱼猎杀速率最终值: {final_d:.2f}")

print("\n注意：实际结果取决于自然增长率r的具体值。")
print("当r较小时，鲨鱼猎杀和鱼类离开的影响会导致鲑鱼数量下降甚至灭绝。")
print("当r足够大时，鲑鱼数量可能会持续增长。")
print("在某些r值下，系统可能会达到平衡状态。")

print("\n添加可视化代码以直观查看不同r值下的种群动态...")

# 创建可视化图表
plt.figure(figsize=(12, 10))

# 短期行为图表 - 鲑鱼数量
plt.subplot(2, 2, 1)
for r_val in r_values:
    plt.plot(t_short, results[r_val]['short'][:, 0], label=f'r = {r_val}')
plt.title('短期行为：鲑鱼数量随时间变化')
plt.xlabel('时间 (分钟)')
plt.ylabel('鲑鱼数量')
plt.grid(True)
plt.legend()

# 短期行为图表 - 鲨鱼猎杀速率
plt.subplot(2, 2, 2)
for r_val in r_values:
    plt.plot(t_short, results[r_val]['short'][:, 1], label=f'r = {r_val}')
plt.title('短期行为：鲨鱼猎杀速率随时间变化')
plt.xlabel('时间 (分钟)')
plt.ylabel('鲨鱼猎杀速率')
plt.grid(True)
plt.legend()

# 长期行为图表 - 鲑鱼数量
plt.subplot(2, 2, 3)
for r_val in r_values:
    plt.plot(t_long, results[r_val]['long'][:, 0], label=f'r = {r_val}')
plt.title('长期行为：鲑鱼数量随时间变化')
plt.xlabel('时间 (分钟)')
plt.ylabel('鲑鱼数量')
plt.grid(True)
plt.legend()

# 长期行为图表 - 鲨鱼猎杀速率
plt.subplot(2, 2, 4)
for r_val in r_values:
    plt.plot(t_long, results[r_val]['long'][:, 1], label=f'r = {r_val}')
plt.title('长期行为：鲨鱼猎杀速率随时间变化')
plt.xlabel('时间 (分钟)')
plt.ylabel('鲨鱼猎杀速率')
plt.grid(True)
plt.legend()

plt.tight_layout()

# 单独创建种群最终状态对比图
plt.figure(figsize=(10, 6))

# 种群最终数量对比
final_p_values = [results[r]['long'][-1, 0] for r in r_values]
plt.bar([f'r={r}' for r in r_values], final_p_values, color='skyblue')
plt.title('不同自然增长率r下的鲑鱼最终数量')
plt.xlabel('自然增长率r')
plt.ylabel('最终鲑鱼数量')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# 添加数值标签
for i, v in enumerate(final_p_values):
    plt.text(i, v, f'{v:.2f}', ha='center', va='bottom')

# 平衡分析
print("\n平衡状态分析:")
for r_val in r_values:
    # 检查是否达到平衡（导数近似为0）
    dpdt_final = r_val * results[r_val]['long'][-1, 0] - results[r_val]['long'][-1, 1] - 0.002
    
    if abs(dpdt_final) < 1:  # 近似平衡条件
        print(f"当r = {r_val}时，系统接近平衡状态，dp/dt = {dpdt_final:.6f}")
    elif dpdt_final > 0:
        print(f"当r = {r_val}时，系统仍在增长，dp/dt = {dpdt_final:.6f}")
    else:
        print(f"当r = {r_val}时，系统仍在减少，dp/dt = {dpdt_final:.6f}")

print("\n可视化图表已创建，运行脚本即可查看。")
print("结论：")
print("1. 系统的长期行为高度依赖于鲑鱼的自然增长率r")
print("2. 当r较小时，鲨鱼猎杀速率最终会导致鲑鱼数量下降")
print("3. 当r足够大时，鲑鱼数量能够持续增长，尽管鲨鱼猎杀速率也在增加")
print("4. 对于特定的r值，系统可能达到平衡状态，此时鲑鱼数量相对稳定")

# 如果需要显示图表，取消下面这行的注释
plt.show()
