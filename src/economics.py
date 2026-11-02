"""
Unit economics for a single 60 kW DC fast charging station.

This is where the project's main finding comes from. The question is not
whether a charger is affordable -- it is whether it gets used enough to pay
for itself. Those are different questions and they have different answers.
"""

# ---- capital cost, rupees ----
CAPEX = {
    "charger_unit_60kw": 500000,
    "installation_civil": 150000,
    "grid_connection": 200000,
    "land_deposit_permits": 150000,
}
TOTAL_CAPEX = sum(CAPEX.values())   # Rs 10,00,000

# Note: the charger itself is only half the cost. Grid connection and land
# are the other half, and they are the two things that actually delay
# projects -- which is part of why ~18% of registered stations are not
# operational.

# ---- operating assumptions ----
CHARGER_KW = 60
HOURS_PER_DAY = 24
PRICE_PER_KWH = 18.0        # what the operator charges the driver
ELECTRICITY_COST_KWH = 9.0  # commercial/EV tariff paid by the operator
ANNUAL_OM = 100000          # maintenance, connectivity, payment gateway, staff

MARGIN_PER_KWH = PRICE_PER_KWH - ELECTRICITY_COST_KWH


def station_economics(utilization_pct, subsidy_pct=0):
    """
    utilization_pct: share of the 24-hour capacity actually delivered.
    subsidy_pct: state capital subsidy on the upfront cost.
    """
    capacity_kwh_day = CHARGER_KW * HOURS_PER_DAY          # 1440
    delivered_kwh_day = capacity_kwh_day * utilization_pct / 100

    gross_margin_year = delivered_kwh_day * MARGIN_PER_KWH * 365
    net_year = gross_margin_year - ANNUAL_OM

    capex = TOTAL_CAPEX * (1 - subsidy_pct / 100)

    if net_year <= 0:
        payback = None          # never pays back
    else:
        payback = capex / net_year

    return {
        "utilization_pct": utilization_pct,
        "subsidy_pct": subsidy_pct,
        "delivered_kwh_day": round(delivered_kwh_day, 1),
        "capex": round(capex),
        "net_annual": round(net_year),
        "payback_years": round(payback, 1) if payback else None,
    }


def breakeven_utilization():
    """
    The utilization at which a station exactly covers its O&M -- below this
    it loses money every year no matter how long you wait.
    """
    capacity = CHARGER_KW * HOURS_PER_DAY
    kwh_needed = ANNUAL_OM / MARGIN_PER_KWH / 365
    return round(100 * kwh_needed / capacity, 2)
