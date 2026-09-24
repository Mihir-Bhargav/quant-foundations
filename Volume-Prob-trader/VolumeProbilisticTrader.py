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
    raw_data = self.market_data.fetch_ticker_data()
    base_df = pd.DataFrame(list(raw_data))
    if base_df.empty: 
      return pd.DataFrame() 

    def extract_trades(row_content): 
      if isinstance(row_content, list) and len(row_content) > 0: 
        event_obj = row_content[0] 
        if isinstance(event_obj, dict): 
          return event_obj.get("trades", [])
      return []

    base_df["extracted_list"] = base_df.iloc[:, 2].apply(extract_trades) 
    df_exploded = base_df.explode("extracted_list") 
    df_flat = pd.json_normalize(df_exploded["extracted_list"]) 
    if df_flat.empty: 
      return df_flat

    df_flat['time'] = pd.to_datetime(df_flat['time'])
    df_flat['price'] = pd.to_numeric(df_flat['price'], errors='coerce')
    df_flat['size'] = pd.to_numeric(df_flat['size'], errors='coerce')
    
    self.live_ticker_data = df_flat.sort_values('time').reset_index(drop=True)
    
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

