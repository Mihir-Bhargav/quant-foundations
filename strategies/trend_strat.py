import yfinance as yf
import numpy as np 

class trend_strategy(): 
    def __init__(self, start, end, ticker):
        self.start = start 
        self.end = end
        self.ticker = ticker
    
    def fetch_data(self, start, end, ticker): 
        data = yf.download(start, end, ticker)
        return data
    
    def test_strat(self): 
        self.fetch_data()
        

