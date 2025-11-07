import numpy as np
import cvxpy as cp

# 变量定义
a1 = cp.Variable(shape=(),name="生产汽油甲的原油A",nonneg=True)
a2 = cp.Variable(shape=(),name="生产汽油乙的原油A",nonneg=True)
b1 = cp.Variable(shape=(),name="生产汽油甲的原油B",nonneg=True)
b2 = cp.Variable(shape=(),name="生产汽油乙的原油B",nonneg=True)
z = cp.Variable(shape=(), name="购买原油A的量", nonneg=True)
cost = cp.Variable(shape=(), name="购买原油A的成本", nonneg=True)

# 目标函数
max = 4800 * (a1+b1) + 5600*(a2+b2)
objective = cp.Maximize(max - cost)

# 约束条件
constraints = []
constraints.append(b1+b2 <= 1000)
constraints.append(a1  >= 0.5*(a1+b1))
constraints.append(a2  >= 0.6*(a2+b2))
constraints.append(z <= 1500)
constraints.append(a1+a2 == 500 + z)

# 分段成本约束（分三段线性化）

# 段1：0 ≤ z ≤ 500，成本 = 10000 * z
z1 = cp.Variable(shape=(), nonneg=True)
constraints.append(z1 <= z)
constraints.append(z1 <= 500)
cost1 = 10000 * z1

# 段2：500 < z ≤ 1000，成本 = 8000 * (z - 500)
z2 = cp.Variable(shape=(), nonneg=True)
constraints.append(z2 <= z - 500)
constraints.append(z2 <= 500)
cost2 = 8000 * z2

# 段3：1000 < z ≤ 1500，成本 = 6000 * (z - 1000)
z3 = cp.Variable(shape=(), nonneg=True)
constraints.append(z3 <= z - 1000)
constraints.append(z3 <= 500)
cost3 = 6000 * z3

constraints.append(z == z1+z2+z3)
# 总成本 = 段1 + 段2 + 段3（段1已包含前500吨的1000元/t成本）
constraints.append(cost == cost1 + cost2 + cost3)

# 构建问题
problem = cp.Problem(objective,constraints)
problem.solve()

print("求解状态:", problem.status)
print("购买原油A的量:大于1000,小于1500")
print("最大利润:", int(problem.value))
print("生产汽油甲的原油A用量:", int(a1.value))
print("生产汽油甲的原油B用量:", int(b1.value))
print("生产汽油乙的原油A用量:", int(a2.value))
print("生产汽油乙的原油B用量:", int(b2.value))
print("采购原油A的量:", int(z.value))
print("原油采购成本:", int(cost.value))
print("原油A的采购量",round(z.value))

