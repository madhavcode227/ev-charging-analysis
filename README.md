# EV Charging Infrastructure — Placement and Viability

A data-led case study on where India's next public EV chargers should go, and
what actually determines whether they pay for themselves.

## The question

India's charging shortfall is normally framed as a counting problem: 27,737
public stations exist, roughly 1.32 million are needed by 2030. That framing
answers *how many* and says nothing about *where* — and the second question is
the one that decides whether the money is wasted.

## What this does

1. Builds state-level metrics from PIB/Ministry of Power and VAHAN data
2. Scores 15 states on placement priority, weighting demand pressure,
   market viability, growth and state subsidy
3. Compares that score against the naive "rank by gap" answer
4. Models the unit economics of a single 60 kW DC station across utilisation
   levels
5. Tests whether capital subsidy rescues a weak site

## Headline findings

**Ranking by gap alone is misleading.** Karnataka ranks 3rd by raw shortfall
but 11th on score — it already has 6,097 stations against 112 EVs each, so it
is the best-served large market in the country. Delhi falls from 6th to 15th
for the same reason. Bihar rises from 10th to 2nd: a thin network against a
fast-growing base.

**Break-even utilisation is 2.11%.** Reported real-world utilisation in India
runs between 1% and 5%. A meaningful share of installed stations therefore sit
at or below the level at which they lose money every year, which is a more
plausible explanation for the ~18% non-operational rate than equipment
failure.

**Utilisation, not capital, is the binding constraint.** At 2% a station never
pays back. At 10% it pays back in 2.7 years with no subsidy at all. A 20%
capital subsidy takes a 10% site from 2.7 to 2.1 years and a 5% site from 7.3
to 5.9 — it improves good sites and does not rescue weak ones.

## Recommendations

1. Shift support from capex to delivered energy (per-kWh), so operators are
   paid for chargers that get used rather than chargers that get installed
2. Select sites by dwell time — highway rest stops, metro parking, bus depots,
   logistics hubs — not by administrative geography
3. Repair the ~4,984 non-operational stations before funding new ones

## Run it

```bash
pip install pandas matplotlib tabulate
python3 src/run.py
```

Regenerates `REPORT.md`, the chart and the CSVs in `outputs/`.

## Layout

```
src/data.py       state dataset, with a note on why sources disagree
src/scoring.py    placement score, weights and rationale
src/economics.py  unit economics for one DC station
src/run.py        analysis, report and chart generation
REPORT.md         generated — full findings
```

## Honest notes

Published station counts disagree by up to 2x across sources depending on
whether they count stations or charging points, and registered or operational
units. One series (PIB) is used throughout — the relative ranking is more
reliable than the absolute values.

Weights are judgment, not fitted to any outcome. A sensitivity check across
weight settings would be the natural next step and is not in this version.

EV registration counts are cumulative and include two- and three-wheelers,
which use public DC charging far less than cars. A category-weighted demand
metric would sharpen the score.
