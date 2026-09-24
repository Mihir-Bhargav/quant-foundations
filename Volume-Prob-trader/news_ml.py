import torch  
import numpy as np 
import pandas as pd 

class news_ml(): 
    def __init__(self, symbol):
        self.symbol = symbol 


    def fetch_news(self): 
        