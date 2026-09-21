# After speaking to an advisor directly to the CIO of Ericsson, there are certain projects he recommended (very impressed by what I did for my age, 16). The core ideas being;
# Play the game of the giants; insitutions place trades with MILLIONS of shares, go with them, not against them.
# Make probabalistic trading strategies with AI instead of set parameters like SMA causing enteries

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
        self.run_websocket() 
        

    def on_message(self, ws, message):
        data = json.loads(message)
        print(data)

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


test = CoinbaseMarketData("BTC-USD")
test.run_websocket() 

