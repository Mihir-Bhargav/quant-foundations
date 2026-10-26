# Quant Foundations

Personal, self-authored quantitative finance and math work — probability &
statistics, stochastic processes, and trading-strategy implementations,
written by me while learning. Separate from
[`Algorithmic_trading_projects`](https://github.com/Mihir-Bhargav/Algorithmic_trading_projects),
which is a larger, AI-assisted trading research and execution system I direct
using Claude Code. This repo is the opposite kind of evidence: everything
here I wrote myself.

## Structure

- **`stochastic-processes-and-pricing/`** — Black-Scholes, Heston via FFT,
  Brownian motion / GBM simulation, Monte Carlo pricing, a volatility dashboard.
- **`backtesting-frameworks/`** — iterative and vectorized backtester
  classes (SMA, mean-reversion, contrarian, ML-based), each subfolder a
  later, more refined pass at the same ideas as I learned more.
- **`machine-learning-for-trading/`** — a DNN model for return prediction,
  plus regression/classification and ML-backtesting notebooks.
- **`broker-integrations/`** — broker API implementations: IBKR and Oanda.
- **`financial-data-analysis/`** — time-series and financial data analysis
  exercises and lecture notebooks.
- **`strategies/`** — standalone strategy implementations (SMA crossover,
  trend-following, a Schrödinger-inspired strategy, portfolio management,
  real-time data handling).
- **`algorithmic-trading-notes/`** — annotated early trading scripts, mostly commentary.
- **`pine-indicators/`** — TradingView Pine Script indicators.

Some concepts (e.g. SMA/mean-reversion backtesters) appear more than once
under `backtesting-frameworks/` — these are genuinely different passes at
the same idea made at different points while learning, kept side by side
rather than collapsed into one "final" version.
