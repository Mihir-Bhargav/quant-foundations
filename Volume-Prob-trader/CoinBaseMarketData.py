# After speaking to an advisor directly to the CIO of Ericsson, there are certain projects he recommended (very impressed by what I did for my age, 16). The core ideas being;
# Play the game of the giants; insitutions place trades with MILLIONS of shares, go with them, not against them.
# Make probabalistic trading strategies with AI instead of set parameters liek SMA causing enteries

# Download these dependencies if not already installed. 
# !pip install yfinance
# !pip install pandas_ta
# !pip install websocket-client

import yfinance as yf
import pandas as pd
import torch
import numpy as np
from torch import nn
import matplotlib.pyplot as plt
import pandas_ta as ta
import websocket
import json
import threading
import time
# These functions help fetch data from coinbase websocket. We can make them into a class, and call this data class from the main trader class.

class CoinbaseMarketData():
  WS_URL = "wss://advanced-trade-ws.coinbase.com"

  def __init__(self, symbol):
    self.symbol = symbol
    self.ticker_data = []
    self.orderflow_data = []
    self.ticker_count = 0
    self.orderflow_count = 0
    self.ws_thread = threading.Thread(target=self.run_websocket, daemon=True)
    self.ws_thread.start()

  def on_open(self, ws):
      # Subscribe to the ticker channel for BTC-USD
      ticker_message = {
          "type": "subscribe",
          "product_ids": [self.symbol],
          "channel": "ticker"
      }
      ws.send(json.dumps(ticker_message))
      print("Subscribed to BTC-USD ticker channel")

      level2_message = {
          "type": "subscribe",
          "product_ids" : [f"{self.symbol}"],
          "channel" : "level2"
      }

      ws.send(json.dumps(level2_message))
      print("Subscribed to BTC-USD level 2 orderflow data")

  def on_message(self, ws, message):
    data = json.loads(message)
    channel = data.get("channel")

    #For Ticker:
    if channel == "ticker":
      self.ticker_data.append(data)
      self.ticker_count +=1
      print("\n---TICKER---")
      print(data)

    elif channel == "l2_data":
      self.orderflow_data.append(data)
      self.orderflow_count +=1

  def on_error(self, ws, error):
    print(f"Error: {error}")

  def on_close(self, ws, close_status_code, close_msg):
    print("Connection Closed")
    print("\n Messages recieved:")
    print("Ticker:", self.ticker_count)
    print("Level 2:", self.orderflow_count)
    if close_status_code or close_msg:
        print("close status code:", close_status_code)
        print("close message:", close_msg)

  def run_websocket(self):
    self.ws_app = websocket.WebSocketApp(
        self.WS_URL,
        on_open = self.on_open,
        on_message=self.on_message,
        on_error=self.on_error,
        on_close=self.on_close,
    )
    self.ws_app.run_forever()

  def get_ticker_data(self):
    return self.ticker_data

  def get_orderflow_data(self):
    return self.orderflow_data


if __name__ == "__main__":
  test = CoinbaseMarketData("BTC-USD")
  time.sleep(5)

  ticker = test.get_ticker_data()
  orderflow = test.get_orderflow_data()

  ticker_channels = {d.get("channel") for d in ticker}
  orderflow_channels = {d.get("channel") for d in orderflow}

  print(f"\nticker_data: {len(ticker)} items, channels present: {ticker_channels}")
  print(f"orderflow_data: {len(orderflow)} items, channels present: {orderflow_channels}")
  print(f"\nSPLIT OK: {ticker_channels <= {'ticker'} and orderflow_channels <= {'l2_data'}}")


