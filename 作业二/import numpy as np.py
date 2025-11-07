import cvxpy as cp

# 定义决策变量
x1 = cp.Variable(nonneg=True)  # 甲用量
x2 = cp.Variable(nonneg=True)  # 乙用量
x3 = cp.Variable(nonneg=True)  # 丁用量
yA = cp.Variable(nonneg=True)  # 混合液用于A
yB = cp.Variable(nonneg=True)  # 混合液用于B
zA = cp.Variable(nonneg=True)  # 丙用于A
zB = cp.Variable(nonneg=True)  # 丙用于B

# 目标函数
profit = 9*(yA + zA) + 15*(yB + zB) - 6*x1 - 16*x2 - 15*x3 - 10*(zA + zB)
objective = cp.Maximize(profit)

# 约束条件
constraints = [
    yA + yB == x1 + x2 + x3,  # 混合液分配
    yA + zA <= 100,           # A需求
    yB + zB <= 200,           # B需求
    x3 <= 50                 # 丁供应
]

# 线性含硫量约束：混合液中原料比例必须满足含硫量要求
# 当混合液用于生产产品时，必须满足这个比例约束
constraints.append(x1 - 3*x2 - 3*x3 <= 0)
# 求解问题
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.ECOS_BB, verbose=False)

# 输出结果
print(f"求解状态: {problem.status}")
print(f"最大利润: {problem.value:.2f} 千元\n")

print("决策变量最优解:")
print(f"原料甲用量 (x1): {x1.value:.2f} 吨")
print(f"原料乙用量 (x2): {x2.value:.2f} 吨")
print(f"原料丁用量 (x3): {x3.value:.2f} 吨")
print(f"混合液用于A (yA): {yA.value:.2f} 吨")
print(f"混合液用于B (yB): {yB.value:.2f} 吨")
print(f"原料丙用于A (zA): {zA.value:.2f} 吨")
print(f"原料丙用于B (zB): {zB.value:.2f} 吨\n")

print("产品生产情况:")
print(f"产品A产量: {yA.value + zA.value:.2f} 吨")
print(f"产品B产量: {yB.value + zB.value:.2f} 吨")