"""
Location data for the House Price Prediction System.

Everything the app knows about places lives in this one file, so adding a
new city or changing a price is a one-line edit.

For every place we store:

    name   - display name
    state  - state / division / district (shown next to the name)
    rate   - typical residential market rate in LOCAL currency per sq ft,
             BEFORE the fame premium is applied. It reflects land cost,
             demand and the local economy of that place.
    fame   - fame / demand score from 1 (little known) to 10 (world famous).
             Famous places (Mumbai, Dhaka, Goa, Cox's Bazar ...) attract
             investors, tourists and migrants, which pushes prices up.

The final rate per sq ft is:

    rate x (1 + FAME_STEP x (fame - 5))

so a fame score of 5 is neutral, 10 adds 15 %, and 1 removes 12 %.

NOTE: the rates are realistic approximations of 2025-26 residential market
levels, intended for a study project. For a production system, refresh them
from a live listing source (99acres, MagicBricks, Bproperty, Lamudi ...).
"""

# Currency of each country.
CURRENCY_SYMBOLS = {
    "India": "\u20b9",        # Rupee sign
    "Bangladesh": "\u09f3",   # Taka sign
}
CURRENCY_NAMES = {
    "India": "INR",
    "Bangladesh": "BDT",
}

# Each +1 of fame score above 5 adds 3 % to the rate (each -1 removes 3 %).
FAME_STEP = 0.03

# Order shown in the dropdowns (largest to smallest settlement).
LOCATION_TYPES = [
    ("Megacity", "Megacity"),
    ("Metropolitan", "Metropolitan City"),
    ("City", "City"),
    ("Village", "Village"),
]


def _p(name, state, rate, fame):
    return {"name": name, "state": state, "rate": rate, "fame": fame}


LOCATIONS = {
    # ------------------------------------------------------------------ INDIA
    # rates in INR per sq ft
    "India": {
        "Megacity": [
            _p("Mumbai", "Maharashtra", 21000, 10),
            _p("Delhi", "NCT of Delhi", 10500, 10),
            _p("Bengaluru", "Karnataka", 8800, 9),
            _p("Kolkata", "West Bengal", 6200, 8),
        ],
        "Metropolitan": [
            _p("Gurugram", "Haryana", 11000, 8),
            _p("Pune", "Maharashtra", 8000, 8),
            _p("Chennai", "Tamil Nadu", 7800, 8),
            _p("Hyderabad", "Telangana", 7500, 8),
            _p("Noida", "Uttar Pradesh", 7000, 7),
            _p("Ahmedabad", "Gujarat", 4800, 7),
        ],
        "City": [
            _p("Panaji (Goa)", "Goa", 8500, 9),
            _p("Chandigarh", "Chandigarh UT", 8200, 7),
            _p("Kochi", "Kerala", 6000, 7),
            _p("Jaipur", "Rajasthan", 4800, 7),
            _p("Visakhapatnam", "Andhra Pradesh", 4600, 6),
            _p("Dehradun", "Uttarakhand", 4500, 6),
            _p("Lucknow", "Uttar Pradesh", 4300, 6),
            _p("Indore", "Madhya Pradesh", 4200, 6),
            _p("Coimbatore", "Tamil Nadu", 4600, 5),
            _p("Surat", "Gujarat", 4300, 5),
            _p("Bhubaneswar", "Odisha", 4000, 5),
            _p("Nagpur", "Maharashtra", 3800, 5),
        ],
        "Village": [
            _p("Kasol", "Himachal Pradesh", 3200, 8),
            _p("Kumarakom", "Kerala", 3800, 7),
            _p("Mawlynnong", "Meghalaya", 1300, 7),
            _p("Sangla", "Himachal Pradesh", 2400, 6),
            _p("Malana", "Himachal Pradesh", 2000, 6),
            _p("Punsari", "Gujarat", 1700, 6),
            _p("Hiware Bazar", "Maharashtra", 1400, 6),
            _p("Khonoma", "Nagaland", 950, 5),
        ],
    },
    # ------------------------------------------------------------ BANGLADESH
    # rates in BDT (Taka) per sq ft
    "Bangladesh": {
        "Megacity": [
            _p("Dhaka", "Dhaka Division", 11500, 10),
        ],
        "Metropolitan": [
            _p("Chattogram", "Chattogram Division", 7500, 9),
            _p("Sylhet", "Sylhet Division", 6200, 7),
            _p("Narayanganj", "Dhaka Division", 5200, 6),
            _p("Khulna", "Khulna Division", 4800, 6),
            _p("Rajshahi", "Rajshahi Division", 4500, 6),
            _p("Gazipur", "Dhaka Division", 4200, 5),
        ],
        "City": [
            _p("Cox's Bazar", "Chattogram Division", 5500, 9),
            _p("Savar", "Dhaka Division", 4800, 5),
            _p("Cumilla", "Chattogram Division", 3600, 5),
            _p("Mymensingh", "Mymensingh Division", 3500, 5),
            _p("Bogura", "Rajshahi Division", 3500, 5),
            _p("Rangpur", "Rangpur Division", 3400, 5),
            _p("Barishal", "Barishal Division", 3300, 5),
            _p("Jashore", "Khulna Division", 3200, 5),
        ],
        "Village": [
            _p("Kuakata", "Patuakhali, Barishal Division", 2600, 7),
            _p("Sajek Valley", "Rangamati, Chattogram Division", 2200, 7),
            _p("Sonargaon (Panam)", "Narayanganj, Dhaka Division", 2000, 6),
            _p("Bichanakandi", "Sylhet Division", 1100, 6),
            _p("Mahasthangarh", "Bogura, Rajshahi Division", 1000, 5),
            _p("Tanguar Haor", "Sunamganj, Sylhet Division", 900, 5),
        ],
    },
}


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def fame_factor(fame):
    """Price multiplier produced by a fame score (5 = neutral)."""
    return 1 + FAME_STEP * (fame - 5)


def fame_label(fame):
    if fame >= 9:
        return "World-famous"
    if fame >= 7:
        return "Very famous"
    if fame >= 5:
        return "Well known"
    return "Lesser known"


def final_rate(place):
    """Rate per sq ft after the fame premium / discount."""
    return place["rate"] * fame_factor(place["fame"])


def get_place(country, location_type, city):
    """Return the place dict, or None if the combination is not valid."""
    for place in LOCATIONS.get(country, {}).get(location_type, []):
        if place["name"] == city:
            return place
    return None


def all_city_choices():
    """Flat list of (name, name) for the form's city field (validation list)."""
    seen, choices = set(), []
    for types in LOCATIONS.values():
        for places in types.values():
            for place in places:
                if place["name"] not in seen:
                    seen.add(place["name"])
                    choices.append((place["name"], place["name"]))
    return choices


def client_data():
    """JSON-serialisable data used by the dependent dropdowns in the browser."""
    cities = {}
    for country, types in LOCATIONS.items():
        cities[country] = {}
        for ltype, places in types.items():
            cities[country][ltype] = [
                {
                    "name": p["name"],
                    "state": p["state"],
                    "fame": p["fame"],
                    "fame_label": fame_label(p["fame"]),
                    "rate": round(final_rate(p)),
                }
                for p in places
            ]
    return {"currency": CURRENCY_SYMBOLS, "cities": cities}
