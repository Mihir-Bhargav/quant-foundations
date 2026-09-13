import yfinance as yf 
import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

ticker = "AAPL"  
start = "2020-01-01" 
end = "2026-01-01" 

data= yf.download(ticker, start, end)
df = pd.DataFrame(data)
print(df)

plt.plot(data["Close"]) 
plt.title("AAPL trading for 2020-2026")
plt.show()


