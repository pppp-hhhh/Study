import sympy as sp  

x = sp.Symbol('x')
expr = (x**2 -1 )/(x-1)
sp.simplify(expr)
sp.expand((x+1)**3)
sp.factor(x**2-5*x + 6)
sp.together(1/(x+1)+ 1/(x+2))
sp.apart((2*x+3)/(x*(x+1)))

y = sp.Function('y')
eq = sp.diff(y(x),x,2) +2*sp.diff(y(x),x) + 2*y(x)
con = {y(0):0,sp.diff(y(x),x).subs(x,0):1}
y = sp.dsolve(eq,ics=con)
print(sp.simplify(y))

t =sp.Symbol('t')
x1,x2,x3 = sp.symbols('x1:4',cls=sp.Function)

x=sp.Matrix([x1(t),x2(t),x3(t)])

A=sp.Matrix([[2,-3,3],[4,-5,3],[4,4,2]])

eq=x.diff(t) - A*x
g = sp.dsolve(eq,ics={x1(0):1,x2(0):2,x3(0):3})
print(g)