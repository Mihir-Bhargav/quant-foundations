import numpy as np 
import sympy as sp 
from sympy import nsolve

## First, there is multivariable funciton
## The goal is to compute the min and max of the function(x, y) with D

#recieve input
function = input("Function minmax, Please enter the multivariable function!")
print(function)

# Calculate the partial derivates as rule 1 
x, y = sp.symbols('x y')
expr = function
f_x = sp.diff(expr, x)
f_y = sp.diff(expr, y)
print(f_x)
print(f_y)

# set both partial derivatives to 0 and return critical points: 
critical_points = sp.solve([f_x, f_y], [x, y])
print(critical_points)

# sp.solve returns a dict for one solution, but a list of tuples for
# several — normalize to always be a list of (x0, y0) so the loop below
# works either way.
if isinstance(critical_points, dict):
    points = [(critical_points[x], critical_points[y])]
else:
    points = critical_points

#take second partial derivatives and the mixed second partial derivative
second_der_x = sp.diff(f_x, x)
second_der_y = sp.diff(f_y, y)
second_der_x_y = sp.diff(f_y, x)
second_der_y_x = sp.diff(f_x, y)
print(second_der_x, second_der_y)
print(second_der_x_y, second_der_y_x)

## Evaluate D and classify AT EACH critical point
for x0, y0 in points:
    fxx = second_der_x.subs({x: x0, y: y0})
    fyy = second_der_y.subs({x: x0, y: y0})
    fxy = second_der_x_y.subs({x: x0, y: y0})
    fyx = second_der_y_x.subs({x: x0, y: y0})

    D = (fxx * fyy) - (fxy * fyx)
    print(f"At ({x0}, {y0}): D = {D}")

    if D > 0 and fxx > 0:
        print(f"  -> local minimum")
    elif D > 0 and fxx < 0:
        print(f"  -> local maximum")
    elif D < 0:
        print(f"  -> saddle point")
    else:
        print(f"  -> inconclusive (D = 0)")

## Sucess! good work!!