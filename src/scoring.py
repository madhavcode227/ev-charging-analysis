"""
Placement scoring model.

The naive answer to "where should the next charger go" is "wherever the gap
is biggest". That answer is wrong, and showing why is the point of this
model.

A large gap can mean two very different things:
  - lots of EVs, not enough chargers  -> a charger here will be busy
  - almost no EVs, so almost no chargers -> a charger here will sit idle

The first is an opportunity. The second is a stranded asset. Gap alone
cannot tell them apart, so the score combines demand pressure with an
absolute viability floor that penalises thin markets.

Weights:
  demand_pressure  0.35  EVs per existing charger -- will it get used
  viability        0.25  absolute EV base -- is the market thick enough
  growth           0.25  YoY EV growth -- infrastructure lasts 10 years,
                         so tomorrow's demand matters as much as today's
  policy           0.15  state capital subsidy -- real but least durable,
                         since policy changes and demand does not

Every input is min-max normalised to 0-100 first, because the raw units
(vehicles, percentages, ratios) are not comparable.
"""

import pandas as pd

WEIGHTS = {
    "demand_pressure": 0.35,
    "viability": 0.25,
    "growth": 0.25,
    "policy": 0.15,
}

BENCHMARK_RATIO = 20    # target EVs per charger


def normalise(s):
    """Min-max to 0-100. Flat series -> all 50, to avoid divide-by-zero."""
    lo, hi = s.min(), s.max()
    if hi == lo:
        return pd.Series(50.0, index=s.index)
    return 100 * (s - lo) / (hi - lo)


def build_metrics(df):
    df = df.copy()

    # How saturated is the existing network
    df["ev_per_charger"] = df["ev_registered"] / df["stations"]

    # How many chargers the benchmark implies, and the shortfall
    df["required_chargers"] = (df["ev_registered"] / BENCHMARK_RATIO).round()
    df["gap"] = df["required_chargers"] - df["stations"]
    df["gap_multiple"] = (df["required_chargers"] / df["stations"]).round(1)

    return df


def score(df):
    df = build_metrics(df)

    df["s_demand"] = normalise(df["ev_per_charger"])
    df["s_viability"] = normalise(df["ev_registered"])
    df["s_growth"] = normalise(df["ev_growth_pct"])
    df["s_policy"] = normalise(df["subsidy_pct"])

    df["score"] = (
        WEIGHTS["demand_pressure"] * df["s_demand"]
        + WEIGHTS["viability"] * df["s_viability"]
        + WEIGHTS["growth"] * df["s_growth"]
        + WEIGHTS["policy"] * df["s_policy"]
    ).round(1)

    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df["rank"] = df.index + 1
    return df


def gap_only_ranking(df):
    """
    The naive ranking, for comparison. If this matches the score ranking,
    the model adds nothing -- so it is worth checking rather than assuming.
    """
    df = build_metrics(df)
    df = df.sort_values("gap", ascending=False).reset_index(drop=True)
    df["gap_rank"] = df.index + 1
    return df[["state", "gap", "gap_rank"]]
