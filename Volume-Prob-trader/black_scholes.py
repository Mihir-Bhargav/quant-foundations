import numpy as np 
import pandas as pd 
import yfinance as yf 

class Black_Scholes(): 
    def __init__(self, symbol, start, end): 
        self.symbol = symbol
        self.start = start 
        self.end  = end 

    def get_data(self): 
        raw = yf.download(self.symbol, self.start, self.end)
        raw.dropna.copy()
        raw = raw.columms[["Close"]] 
        print(raw) 

    def compute_call_prices(self, rfr, t, vol): 
        

test = Black_Scholes("AAPL", "2020-01-01", "2026-01-01")
