# After speaking to an advisor directly to the CIO of Ericsson, there are certain projects he recommended (very impressed by what I did for my age, 16). The core ideas being;
# Play the game of the giants; institutions place trades with MILLIONS of shares, go with them, not against them.
# Make probabilistic trading strategies with AI instead of set parameters like SMA causing entries

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

# These functions help fetch data from Coinbase websocket.
# We can make them into a class, and call this data class from the main trader class.

class CoinbaseMarketData():

    WS_URL = "wss://advanced-trade-ws.coinbase.com"

    def __init__(self, symbol):
        self.symbol = symbol
        self.ticker_data = []
        self.orderflow_data = []

        self.ws_thread = threading.Thread(target=self.run_websocket, daemon=True)
        self.ws_thread.start()

    def on_message(self, ws, message):
        data = json.loads(message)
        channel = data.get("channel")

        if channel == "market_trades":
            self.ticker_data.append(data)

        elif channel == "l2_data":
            self.orderflow_data.append(data)
 

    def on_error(self, ws, error):
        print("ERROR:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("CLOSED:", close_status_code, close_msg)

    def on_open(self, ws):
        print("Connected!")

        ws.send(json.dumps({
            "type": "subscribe",
            "product_ids": [self.symbol],
            "channel": "market_trades"
        }))

        ws.send(json.dumps({
            "type": "subscribe",
            "product_ids": [self.symbol],
            "channel": "level2"
        }))

    def run_websocket(self):
        self.ws = websocket.WebSocketApp(
            self.WS_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        self.ws.run_forever()

    def fetch_orderflow_data(self): 
        print(len(self.orderflow_data))
        return self.orderflow_data

    def fetch_ticker_data(self): 
        print(len(self.ticker_data))
        return self.ticker_data
      

if __name__ == "__main__":
    test = CoinbaseMarketData("BTC-USD")
    time.sleep(5)
    test.fetch_orderflow_data()
    test.fetch_ticker_data()
