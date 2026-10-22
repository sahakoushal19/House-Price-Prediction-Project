"""
Price calculation and money formatting.

Kept free of Django imports so it can be tested on its own.

How the final price is built
----------------------------
1. The trained ML model (LinearRegression) predicts a BASE price from the
   property itself: area, bedrooms, bathrooms, stories, parking.
   That base price is "location-neutral" - it is the value of the same house
   in an average market, whose rate is about BASELINE_RATE per sq ft
   (training-data mean price / mean area = 8.71M / 2813 sq ft = ~3,100).

2. The chosen place scales the base price:

       market_index = place rate per sq ft / BASELINE_RATE
       fame_factor  = 1 + 3 % per fame point above 5
       multiplier   = market_index x fame_factor

3. final price = base price x multiplier
"""

from .locations import (
    CURRENCY_NAMES,
    CURRENCY_SYMBOLS,
    fame_factor,
    fame_label,
    final_rate,
    get_place,
)

# Average rate per sq ft implied by the data the model was trained on.
BASELINE_RATE = 3100.0

# The estimate is shown with a +/- band, because no model is exact.
RANGE_PERCENT = 0.08


def group_indian(number):
    """12345678 -> '1,23,45,678' (lakh / crore digit grouping)."""
    n = int(round(abs(number)))
    s = str(n)
    if len(s) <= 3:
        grouped = s
    else:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        grouped = ",".join(parts + [tail])
    return ("-" if number < 0 else "") + grouped


def short_words(value):
    """28400000 -> '2.84 Crore', 450000 -> '4.50 Lakh'."""
    if value >= 1e7:
        return f"{value / 1e7:.2f} Crore"
    if value >= 1e5:
        return f"{value / 1e5:.2f} Lakh"
    return group_indian(value)


def money(value, country):
    """Full amount with the currency symbol, e.g. '₹ 2,84,00,000'."""
    return f"{CURRENCY_SYMBOLS[country]} {group_indian(value)}"


def estimate_price(base_price, country, location_type, city):
    """Apply the city's market level and fame to the ML base price."""
    place = get_place(country, location_type, city)
    if place is None:
        raise ValueError(f"Unknown place: {city} ({location_type}, {country})")

    base_price = max(float(base_price), 0.0)

    market_index = place["rate"] / BASELINE_RATE
    fame = fame_factor(place["fame"])
    multiplier = market_index * fame
    price = round(base_price * multiplier, 2)

    low = price * (1 - RANGE_PERCENT)
    high = price * (1 + RANGE_PERCENT)

    return {
        "price": price,
        "price_full": money(price, country),
        "price_words": f"{CURRENCY_SYMBOLS[country]} {short_words(price)}",
        "range_text": f"{CURRENCY_SYMBOLS[country]} {short_words(low)}  -  {short_words(high)}",
        "symbol": CURRENCY_SYMBOLS[country],
        "currency": CURRENCY_NAMES[country],
        "base_price": round(base_price, 2),
        "base_price_full": money(base_price, country),
        "multiplier": round(multiplier, 4),
        "market_index": round(market_index, 2),
        "fame_score": place["fame"],
        "fame_label": fame_label(place["fame"]),
        "fame_percent": round((fame - 1) * 100),
        "city": place["name"],
        "state": place["state"],
        "country": country,
        "location_type": location_type,
        "rate_final": money(final_rate(place), country),
    }
