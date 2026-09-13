import pandas as pd 
import yfinance as yf 
import matplotlib.pyplot as plt 
import numpy as np 

class SMABacktester():
    def __init__(self, symbol, start, end, sma_l, sma_s):
        self.symbol = symbol 
        self.start = start 
        self.end = end 
        self.sma_l = sma_l 
        self.sma_s = sma_s
        self.get_data()
        self.prepare_data()

    def __repr__(self):
        return "SMABacktester(symbol = {}, SMA_S = {}, SMA_L = {}, start = {}, end = {})".format(self.symbol, self.SMA_S, self.SMA_L, self.start, self.end)

    def get_data(self): 
        data = yf.download(self.symbol, self.start, self.end) 
        df = pd.DataFrame(data)
        df.columns = df.columns.get_level_values(0)
        df = df.reset_index()
        df = df[["Date", "Close", "Volume"]]
        df = df.rename(columns={'Close': 'Price'})
        df.set_index('Date')
        self.data = df

    def prepare_data(self):
        df = self.data.copy()
        df["sma_s"] = df["Price"].rolling(self.sma_s).mean() 
        df["sma_l"] = df["Price"].rolling(self.sma_l).mean()
        df["returns"] = np.log(df["Price"]/df["Price"].shift(1)) 
        self.df = df
        print(df)

    def test_strategy(self):
        df = self.df.copy().dropna()
        df["position"] = np.where(df["sma_s"] > df["sma_l"], 1, -1)
        df["strategy"] = df["position"].cumsum().apply(np.exp)
        df.dropna(inplace=True) 
        df["creturns"] = df["returns"].cumsum().apply(np.exp)
        df["cstrategy"] = df["strategy"].cumsum().apply(np.exp)
        self.results = df

        perf = df["cstrategy"].iloc[-1] 
        outperf = perf - df["creturns"].iloc[-1] 
        return round(perf, 6), round(outperf, 6)

    def plot_results(self):
        if self.results is None:
            print("Run test_strategy() first.")
        else:
            title = "{} | SMA_S = {} | SMA_L = {}".format(self.symbol, self.SMA_S, self.SMA_L)
            self.results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))

        

sma = SMABacktester("AAPL", "2020-01-01", "2026-01-01", 14, 20) 
sma.prepare_data()