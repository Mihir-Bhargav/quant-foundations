import numpy as np 
import math 

class math_calc(): 
    def __init__(self, f): 
        self.f = f
        

    def calculate_derivative(self, x, h=1e-7): 
        self.derivative = (self.f(x + h) - self.f(x - h)) / (2 * h)
        print(f"The derivative at x={x} is: {round(self.derivative, 2)}")
        return round(self.derivative, 2) 
    
    def solve_functions(self): 
        pass

test = math_calc(lambda x: 3 * x**4)
print(test.calculate_derivative(4))   
