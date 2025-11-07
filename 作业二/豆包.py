import cvxpy as cp

# 1. 定义变量
# 生产汽油甲的原油A、B用量
x1 = cp.Variable(shape=(), name="GasolineA_CrudeA", nonneg=True)
y1 = cp.Variable(shape=(), name="GasolineA_CrudeB", nonneg=True)
# 生产汽油乙的原油A、B用量
x2 = cp.Variable(shape=(), name="GasolineB_CrudeA", nonneg=True)
y2 = cp.Variable(shape=(), name="GasolineB_CrudeB", nonneg=True)
# 采购原油A的量
z = cp.Variable(shape=(), name="Purchase_CrudeA", nonneg=True)
# 原油采购成本（辅助变量，分三段计算）
cost = cp.Variable(shape=(), name="Purchase_Cost", nonneg=True)

# 2. 目标函数：最大化利润（收入 - 成本）
# 汽油甲收入：4800 * (x1 + y1)；汽油乙收入：5600 * (x2 + y2)
revenue = 4800 * (x1 + y1) + 5600 * (x2 + y2)
objective = cp.Maximize(revenue - cost)

# 3. 约束条件
constraints = []
# 原油A总量约束：库存500吨 + 采购z吨 = 汽油甲用x1 + 汽油乙用x2
constraints.append(x1 + x2 == 500 + z)
# 原油B总量约束：库存1000吨 = 汽油甲用y1 + 汽油乙用y2
constraints.append(y1 + y2 == 1000)
# 汽油甲中原油A占比 > 50%：x1 / (x1 + y1) > 0.5 → x1 > y1
constraints.append(x1 >= 0.5 * (x1 + y1))
# 汽油乙中原油A占比 > 60%：x2 / (x2 + y2) > 0.6 → x2 > 1.5 * y2
constraints.append(x2 >= 0.6 * (x2 + y2))
# 采购量限制：不超过1500吨
constraints.append(z <= 1500)

# 分段成本约束（分三段线性化）
# 段1：0 ≤ z ≤ 500，成本 = 10000 * z
z1 = cp.Variable(shape=(), nonneg=True)
constraints.append(z1 <= z)
constraints.append(z1 <= 500)
cost1 = 10000 * z1

# 段2：500 < z ≤ 1000，成本 = 8000 * (z - 500)（超出500的部分）
z2 = cp.Variable(shape=(), nonneg=True)
constraints.append(z2 <= z - 500)
constraints.append(z2 <= 500)
cost2 = 8000 * z2

# 段3：1000 < z ≤ 1500，成本 = 6000 * (z - 1000)（超出1000的部分）
z3 = cp.Variable(shape=(), nonneg=True)
constraints.append(z3 <= z - 1000)
constraints.append(z3 <= 500)
cost3 = 6000 * z3

# 总成本 = 段1 + 段2 + 段3（段1已包含前500吨的1000元/t成本）
constraints.append(z == z1 + z2 + z3)
constraints.append(cost == cost1 + cost2 + cost3)

# 4. 构建并求解问题
problem = cp.Problem(objective, constraints)
problem.solve(solver=cp.ECOS)  # 可选用GUROBI、ECOS等求解器，若无商业求解器，默认用ECOS

# 5. 输出结果
print("求解状态:", problem.status)
print("最大利润:", round(problem.value))
print("生产汽油甲的原油A用量:", round(x1.value))
print("生产汽油甲的原油B用量:", round(y1.value))
print("生产汽油乙的原油A用量:", round(x2.value))
print("生产汽油乙的原油B用量:", round(y2.value))
print("采购原油A的量:", round(z.value))
print("原油采购成本:", round(cost.value))
print("原油A的采购量",round(z.value))