import sympy as sp

# 定义时间t
t = sp.symbols('t')
# p是鲑鱼t时刻的总数，d是鲨鱼猎杀鲑鱼的速率
p = sp.Function('p')(t)
d = sp.Function('d')(t)

# 鲑鱼增长速率 sp.diff(d,t) = 0.003*p
# t==0 , d == 0.001*p**2
# 平均每分钟有0.002条鱼离开阿拉斯加水域

# 修正后Malthus生物总数增长率
true_speed_p = sp.diff(p,t) - 0.001*p**2 - 0.002

# 定义约束条件
cons = []

sp.Eq()