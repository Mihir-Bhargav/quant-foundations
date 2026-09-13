import pandas as pd 
import numpy as np 
import yfinance as yf
from IterativeBase import IterativeBase

class SMA_backtester(): 
    def __init__(self, sma_long, sma_short, ticker, start, end): 
        self.sma_short = sma_short
        self.sma_long = sma_long 
        self.start = start 
        self.end = end 
        self.ticker = ticker 

    def fetch_data(self): 
        IterativeBase.get_data()
    
    def sma_backtester(self, sma_long, sma_short):
        

