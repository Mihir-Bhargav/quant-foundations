import torch  
import numpy as np 
import pandas as pd 
import requests 


class news_ml(): 
    def __init__(self, symbol):
        self.symbol = symbol 

    def fetch_news(self):
        self.r = requests.get("https://cryptocurrency.cv/api/news", params={"limit": 20}, timeout=10)
        print(self.r.status_code)
        print(self.r.url)
        data = self.r.json() 
        print(type(data), data.keys())
        print(".")

if __name__ == "__main__": 
    news = news_ml("BTC-USD")  
    news.fetch_news()




        


        