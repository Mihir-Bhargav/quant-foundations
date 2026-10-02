import numpy as np 
import math 

class math_calc(): 
    def __init__(self): 
        pass 

    def calculate_derivative(self, f, x, h=1e-7): 
        self.derivative = (f(x + h) - f(x - h)) / (2 * h)
        print(f"The derivative at x={x} is: {round(self.derivative, 2)}")
        return round(self.derivative, 2)
              
test = math_calc()
my_function = lambda x: 3 * x**4
print(test.calculate_derivative(my_function, 4))   
