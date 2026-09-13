
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from itertools import product
plt.style.use("seaborn-v0_8")


class SMABacktester():
    ''' Class for the vectorized backtesting of SMA-based trading strategies.
    '''
    
    def __init__(self, symbol, SMA_S, SMA_L, start, end):
        '''
        Parameters
        ----------
        symbol: str
            ticker symbol (instrument) to be backtested
        SMA_S: int
            moving window in bars (e.g. days) for shorter SMA
        SMA_L: int
            moving window in bars (e.g. days) for longer SMA
        start: str
            start date for data import
        end: str
            end date for data import
        '''
        self.symbol = symbol
        self.SMA_S = SMA_S
        self.SMA_L = SMA_L
        self.start = start
        self.end = end
        self.results = None 
        self.get_data()
        self.prepare_data()
        
    def __repr__(self):
        return "SMABacktester(symbol = {}, SMA_S = {}, SMA_L = {}, start = {}, end = {})".format(self.symbol, self.SMA_S, self.SMA_L, self.start, self.end)
        
    def get_data(self):
        ''' Imports the data from yfinance.
        '''
        raw = yf.download(self.symbol, start = self.start, end = self.end,
                           auto_adjust = True, progress = False)
        raw = raw["Close"].dropna()
        raw.columns = ["price"]
        # Log returns, not simple returns: they're additive over time (r1+r2+...),
        # which is what lets cumsum().apply(np.exp) later reconstruct compounded growth.
        raw["returns"] = np.log(raw["price"] / raw["price"].shift(1))
        self.data = raw

    def prepare_data(self):
        '''Prepares the data for strategy backtesting (strategy-specific).
        '''
        data = self.data.copy()
        # Two moving averages of the SAME price series, just different lookback windows.
        # SMA_S reacts faster to recent price action; SMA_L is the slower "trend" baseline.
        data["SMA_S"] = data["price"].rolling(self.SMA_S).mean()
        data["SMA_L"] = data["price"].rolling(self.SMA_L).mean()
        self.data = data
        
    def set_parameters(self, SMA_S = None, SMA_L = None):
        ''' Updates SMA parameters and the prepared dataset.
        '''
        if SMA_S is not None:
            self.SMA_S = SMA_S
            self.data["SMA_S"] = self.data["price"].rolling(self.SMA_S).mean()
        if SMA_L is not None:
            self.SMA_L = SMA_L
            self.data["SMA_L"] = self.data["price"].rolling(self.SMA_L).mean()
            
    def test_strategy(self):
        ''' Backtests the SMA-based trading strategy.
        '''
        data = self.data.copy().dropna()
        # THE SIGNAL — always in the market, never flat:
        #   SMA_S > SMA_L  -> short-term trend is above the long-term trend -> go LONG  ( 1)
        #   SMA_S <= SMA_L -> short-term trend is below/equal the long-term  -> go SHORT (-1)
        # This is a classic golden-cross / death-cross crossover, just vectorized over the
        # whole series instead of checked bar-by-bar.
        data["position"] = np.where(data["SMA_S"] > data["SMA_L"], 1, -1)

        # .shift(1) is the critical no-lookahead-bias line: today's SMA values (and therefore
        # today's position) are only known using today's closing price, so we can't apply that
        # same day's position to that same day's return — that would be trading on information
        # you don't have until the close. Shifting by 1 means "yesterday's position decides
        # what happens to today's return", i.e. you'd have entered at yesterday's close.
        data["strategy"] = data["position"].shift(1) * data["returns"]
        data.dropna(inplace=True)

        # Log returns are additive, so summing them and exponentiating turns the running total
        # back into a compounded growth factor (1.0 = breakeven, 1.5 = +50% cumulative, etc.).
        # creturns = passive buy-and-hold benchmark; cstrategy = the long/short SMA strategy.
        data["creturns"] = data["returns"].cumsum().apply(np.exp)
        data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
        self.results = data

        perf = data["cstrategy"].iloc[-1] # absolute performance of the strategy
        outperf = perf - data["creturns"].iloc[-1] # out-/underperformance of strategy
        return round(perf, 6), round(outperf, 6)
    
    def plot_results(self):
        ''' Plots the performance of the trading strategy and compares to "buy and hold".
        '''
        if self.results is None:
            print("Run test_strategy() first.")
        else:
            title = "{} | SMA_S = {} | SMA_L = {}".format(self.symbol, self.SMA_S, self.SMA_L)
            self.results[["creturns", "cstrategy"]].plot(title=title, figsize=(12, 8))
    
    def optimize_parameters(self, SMA_S_range, SMA_L_range):
        ''' Finds the optimal strategy (global maximum) given the SMA parameter ranges.

        Parameters
        ----------
        SMA_S_range, SMA_L_range: tuple
            tuples of the form (start, end, step size)
        '''
        
        # Brute-force grid search: every (SMA_S, SMA_L) pair from the two ranges, e.g.
        # range(10, 50, 5) x range(100, 252, 10) -> every combination gets backtested.
        combinations = list(product(range(*SMA_S_range), range(*SMA_L_range)))

        # test all combinations
        results = []
        for comb in combinations:
            self.set_parameters(comb[0], comb[1])          # re-run prepare_data's rolling means
            results.append(self.test_strategy()[0])        # store just the absolute performance

        best_perf = np.max(results) # best performance
        opt = combinations[np.argmax(results)] # optimal parameters

        # NOTE: this optimizes purely on the historical/in-sample performance number — there's
        # no train/test split here, so the "best" combo is by definition overfit to this exact
        # date range. Good for explaining the mechanics; not evidence the combo will hold up
        # out-of-sample without a proper walk-forward or holdout test.

        # run/set the optimal strategy
        self.set_parameters(opt[0], opt[1])
        self.test_strategy()

        # create a df with many results
        many_results =  pd.DataFrame(data = combinations, columns = ["SMA_S", "SMA_L"])
        many_results["performance"] = results
        self.results_overview = many_results

        return opt, best_perf


if __name__ == "__main__":
    tester = SMABacktester(symbol = "EURUSD=X", SMA_S = 50, SMA_L = 200,
                            start = "2004-01-01", end = "2020-06-30")
    print(tester)

    perf, outperf = tester.test_strategy()
    print("Absolute performance: {} | Out-/underperformance vs. buy-and-hold: {}".format(perf, outperf))

    tester.set_parameters(SMA_S = 20, SMA_L = 100)
    perf, outperf = tester.test_strategy()
    print("After set_parameters(20, 100) -> performance: {} | out-/underperformance: {}".format(perf, outperf))

    tester.plot_results()
    plt.savefig("sma_backtest_results.png")
    print("Saved plot to sma_backtest_results.png")

    opt, best_perf = tester.optimize_parameters(SMA_S_range = (10, 50, 5), SMA_L_range = (100, 252, 10))
    print("Optimal (SMA_S, SMA_L): {} | Best performance: {}".format(opt, best_perf))
    print(tester.results_overview.sort_values("performance", ascending = False).head())

