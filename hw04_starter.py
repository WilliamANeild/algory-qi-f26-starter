"""Homework 4 starter — Algory QI Education, Fall 2026

The backtester is the piece worth getting right. Everything after it in the
semester assumes it works.
"""
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

LOOKBACK = 60


# ---------------------------------------------------------------- Q1
def load_and_split(split_date="2011-09-09", prices=None, warmup=LOOKBACK):
    """Split ^SP500TR since 1990 into training and test at `split_date`.

    Training ends on the split date's close. Test begins `warmup` trading days
    BEFORE it, so the 60-day window is already full on the first day traded out
    of sample. Those overlapping days are history the strategy reads, never days
    it earns a return on. Cut the series at one date with no overlap and the
    first 60 days of the test set have no window, so the out-of-sample period
    silently starts three months late.

    September 9, 2011 is a Friday. A split date has to be a trading day, or
    "ends on that close" names a close that does not exist.

    Pass `prices` to split a series you already have, which is how the checker
    tests this without a download. Return (training, test).
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- Q2, Q4, Q5
def always_hold(window):
    """Always invest. The control case, and the one that proves the backtester."""
    return True


def always_cash(window):
    """Never invest. Must produce exactly 0% return."""
    return False


def make_random_hold(p=0.7, seed=0):
    """Return a strategy that invests with probability p each day.

    A factory, not a plain function, because the generator has to live somewhere
    and a default argument is the wrong place: `rng=np.random.default_rng(0)` in
    a signature is evaluated once when the module loads, so every backtest in the
    session shares one advancing generator and the same backtest returns a
    different number each time you run it. Building the generator here gives one
    per strategy, so `backtest(train, make_random_hold())` is reproducible.
    """
    rng = np.random.default_rng(seed)

    def random_hold(window):
        return bool(rng.random() < p)

    return random_hold


def five_day_reversal(window):
    """The rule from class: hold unless the last 5 days were positive.

    Measure that return from the close 5 days before today to today's close,
    both of which are inside the window.
    """
    # TODO
    raise NotImplementedError


def my_strategy(window):
    """Your own rule. It sees only `window`, the previous LOOKBACK closes.

    It must never look at anything after that. That is the whole assignment.
    """
    # TODO
    raise NotImplementedError


# ---------------------------------------------------------------- Q3
def backtest(prices, strategy, lookback=LOOKBACK):
    """Walk forward one day at a time and apply the strategy's decision.

    The convention, stated exactly, because everything else depends on it:

        on day i, the strategy is handed prices[i - lookback + 1 : i + 1],
        the `lookback` closes ENDING WITH today's, today's included;
        if it says hold you earn prices[i + 1] / prices[i] - 1, otherwise zero.

    So i runs from lookback - 1 to len(prices) - 2. The first decision is made on
    the 60th close and the first return earned runs from the 60th close to the
    61st. Today's close is known when you decide, so withholding it throws away a
    day of information for nothing; tomorrow's close is what you are predicting,
    so reading it is the bug this whole session is about.

    Return a dict with at least:
        total_return, annualised_return, max_drawdown, fraction_invested

    Annualise by trading days, 252 a year, compounded: value ** (252 / days) - 1.

    Sanity checks before you trust it:
        always_hold  must match buy-and-hold over the days actually traded,
                     prices[-1] / prices[lookback - 1] - 1, not over the
                     whole file
        always_cash  must return exactly 0.0
    If either fails you have an off-by-one, and every number after it is fiction.
    """
    # TODO
    raise NotImplementedError


def main():
    train, test = load_and_split()
    for name, strat in [("always hold", always_hold),
                        ("always cash", always_cash),
                        ("random 70%", make_random_hold(0.7, seed=0)),
                        ("5-day reversal", five_day_reversal)]:
        r = backtest(train, strat)
        print(f"{name:<16} total {r['total_return']:+.1%}   annual {r['annualised_return']:+.2%}")
    # TODO: Q6 — print EVERY variant you try, not just the one you keep
    # TODO: Q8 — run my_strategy on the test set. Once.
    # TODO: Q9 — what does your rule say to do today?


if __name__ == "__main__":
    main()
