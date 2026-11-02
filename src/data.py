"""
State-level EV and charging infrastructure data.

Source: PIB / Ministry of Power figures as reported for 2025-26.

A note on why the source matters. Published estimates for the same state
disagree by up to 2x -- one widely-cited source puts Karnataka at 6,097
stations, another at 2,900. The disagreement comes from three things:

  1. "Charging station" vs "charging point" -- one station can hold several
     points, and sources rarely say which they are counting.
  2. Registered vs operational -- roughly 18% of registered stations are not
     working at any given time.
  3. Different snapshot dates in a market growing ~40% a year.

So the first analytical decision here was to fix one source and stay on it,
rather than mix the best-sounding number from each. Everything below uses the
PIB series. Absolute values may be off; the relative ranking is what the
analysis actually rests on.
"""

import pandas as pd

# stations: public charging stations, PIB series
# ev_registered: cumulative registered EVs (all vehicle categories), VAHAN
# ev_growth_pct: approximate YoY growth in EV registrations
# capital_subsidy_pct: state capital subsidy on charging infrastructure
STATE_DATA = [
    # state,            stations, ev_registered, ev_growth_pct, subsidy_pct
    ("Karnataka",          6097,      680000,          38,          10),
    ("Maharashtra",        4155,      920000,          42,          15),
    ("Uttar Pradesh",      2326,     1450000,          35,          20),
    ("Delhi",              1967,      400000,          28,          10),
    ("Tamil Nadu",         1781,      480000,          45,          10),
    ("Gujarat",            1200,      350000,          40,          10),
    ("Kerala",              950,      260000,          48,           0),
    ("Rajasthan",           850,      520000,          36,           0),
    ("Telangana",           820,      230000,          44,          10),
    ("Haryana",             700,      280000,          33,           0),
    ("West Bengal",         620,      310000,          30,           0),
    ("Madhya Pradesh",      580,      340000,          34,           0),
    ("Andhra Pradesh",      540,      240000,          37,          10),
    ("Punjab",              420,      190000,          31,           0),
    ("Bihar",               380,      290000,          39,           0),
]

NATIONAL = {
    "stations_registered": 27737,
    "stations_operational": 22753,
    "ev_charger_ratio": 235,          # EVs per public charging station
    "benchmark_ratio_low": 6,          # global benchmark band
    "benchmark_ratio_high": 20,
    "required_2030": 1320000,          # ORF estimate for 30% EV penetration
    "pm_edrive_allocation_cr": 2000,
    "pm_edrive_target_stations": 72300,
}


def load_states():
    df = pd.DataFrame(
        STATE_DATA,
        columns=["state", "stations", "ev_registered",
                 "ev_growth_pct", "subsidy_pct"],
    )
    return df
