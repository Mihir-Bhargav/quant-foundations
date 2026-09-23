from CoinBaseMarketData import CoinbaseMarketData
import yfinance as yf
import pandas as pd
import torch
import numpy as np
from torch import nn
import matplotlib.pyplot as plt
import matplotlib.animation 
from matplotlib.animation import FuncAnimation
import pandas_ta as ta
import websocket
import json
import time

class VolumeProbabilsticTrader():
  def __init__(self, symbol, start, end):
    self.start = start
    self.symbol = symbol
    self.end = end
    self.data = None
    self.market_data = CoinbaseMarketData(self.symbol)
    time.sleep(5)  
    self.get_live_data()
    self.get_orderflow_live()

  def __repr__(self):
    return "VolumeProbabilisticTrader(symbol = {}, start = {}, end = {})".format(self.symbol, self.start, self.end)

  def get_live_data(self):
    self.live_ticker_data = self.market_data.fetch_ticker_data()
    self.live_ticker_data = pd.DataFrame(list(self.live_ticker_data))
    print(self.live_ticker_data)
    return self.live_ticker_data

  def get_orderflow_live(self):
    self.live_order_data = self.market_data.fetch_orderflow_data()
    self.live_order_data = pd.DataFrame(list(self.live_order_data))
    print(self.live_order_data)
    return self.live_order_data 

  def prepare_price_features(self):
    data = self.data.copy()
    data["SMA_S"] = data["price"].rolling(50).mean()
    data["SMA_L"] = data["price"].rolling(200).mean()
    data["rsi"] = data.ta.rsi(close="price", length=14)
    data = data.dropna()
    self.data = data
    return self.data

  def plot_live_ticker(self): 
    self.live_ticker_data.copy() 
    plt.ion() 
    

if __name__ == "__main__":
  tester = VolumeProbabilsticTrader("BTC-USD", "2020-01-01", "2026-01-01")
  tester.get_live_data()
  tester.get_orderflow_live()

  try:
    while True:
      time.sleep(5)
      print(f"ticker: {len(tester.market_data.ticker_data)} rows | orderflow: {len(tester.market_data.orderflow_data)} rows")
  except KeyboardInterrupt:
    print("Stopped.")

