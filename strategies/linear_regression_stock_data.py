import yfinance as yf 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

## first fetch data 
ticker = "AAPL"
start = "2026-01-01"
end = "2026-07-01"

data = yf.download(ticker, start, end)
df = pd.DataFrame(data)
df.columns = df.columns.get_level_values(0)
df = df.reset_index()
df = df[["Date", "Close", "Volume"]]
df = df.rename(columns={'Close': 'Price'})
df.set_index('Date')
df["returns"] = np.log(df["Price"]/df["Price"].shift(1))
df = df.dropna()
print(df)


df["day"] = np.arange(len(df))
x = df[["day"]]
y = df[["returns"]]
model = LinearRegression()
model.fit(x, y)

plt.scatter(df["Date"], df["returns"])
plt.plot(df["Date"], model.predict(x), color="red")
plt.ylim(-0.1, 0.1)
plt.title("Returns for Apple from 2000-2026")
plt.show()

future_days = np.arange(len(df), len(df) + 30).reshape(-1, 1)
predicted_returns = model.predict(future_days).flatten()

last_price = df["Price"].iloc[-1]
predicted_prices = last_price * np.exp(np.cumsum(predicted_returns))

print(predicted_prices)
plt.plot(predicted_prices)
plt.show()



