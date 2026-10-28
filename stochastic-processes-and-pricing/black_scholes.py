import numpy as np 
import pandas as pd 
import yfinance as yf 
import math 
import scipy 
from scipy.stats import norm

class Black_Scholes(): 
    def __init__(self): 
        pass

    def compute_theo_call(self, s, k, r, t, vol): 
        d1 = (math.log(s/k) + (r + 0.5*(vol**2)*t))/(vol * math.sqrt(t))
        d2 = d1 - (vol * math.sqrt(t))
        call_price = (s * norm.cdf(d1) - (k* np.exp(-r * t)) * norm.cdf(d2)) 
        call_price = round(call_price, 3) 
        print(f"The theoretical call price of the parameters is : {call_price}") 
        return call_price

    def compute_put_price(self, s, k, r, t, vol): 
        d1 = (math.log(s/k) + (r + 0.5*(vol**2)*t))/(vol * math.sqrt(t))
        d2 = d1 - (vol * math.sqrt(t)) 
        put_price = 



test = Black_Scholes() 
print(test.compute_theo_call(100, 100, 0.05, 1.0, 0.20)) 

