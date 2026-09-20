from CoinBaseMarketData import CoinbaseMarketData
import yfinance as yf
import pandas as pd
import torch
import numpy as np
from torch import nn
import matplotlib.pyplot as plt
import pandas_ta as ta
import websocket
import json

class VolumeProbabilsticTrader():
  def __init__(self, symbol, start, end, ):
    self.start = start
    self.symbol = symbol
    self.end = end
    self.get_data()
    self.market_data = CoinbaseMarketData(self.symbol)

  def __repr__(self):
    return "VolumeProbabilisticTrader(symbol = {}, start = {}, end = {})".format(self.symbol, self.start, self.end)

  def get_data(self):
    raw = yf.download(self.symbol, self.start, self.end)
    raw = raw["Close"].dropna()
    raw.columns = ["price"]
    raw["returns"] = np.log(raw["price"]/ raw["price"].shift(1))
    self.data = raw
    return self.data

  def get_orderflow_data(self):
    return self.market_data.get_orderflow_data()

  def prepare_price_features(self):
    # In this function, we will have to fetch level 2 data from Thompson Reuters
    data = self.data.copy()
    data["SMA_S"] = data["price"].rolling(50).mean()
    data["SMA_L"] = data["price"].rolling(200).mean()
    data["rsi"] = data.ta.rsi(close="price", length=14)
    data = data.dropna()
    self.data = data
    return self.data 

tester = VolumeProbabilsticTrader("BTC-USD", "2020-01-01", "2026-01-01")
tester.get_orderflow_data()

