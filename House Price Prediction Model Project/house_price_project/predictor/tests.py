from django.test import SimpleTestCase

from .locations import LOCATIONS, get_place, final_rate
from .pricing import estimate_price, group_indian, short_words, BASELINE_RATE


class LocationDataTests(SimpleTestCase):
    def test_every_country_has_all_four_types(self):
        for country, types in LOCATIONS.items():
            for ltype in ("Megacity", "Metropolitan", "City", "Village"):
                self.assertTrue(types[ltype], f"{country} has no {ltype}")

    def test_city_names_are_unique(self):
        names = [p["name"] for t in LOCATIONS.values() for ps in t.values() for p in ps]
        self.assertEqual(len(names), len(set(names)))

    def test_hierarchy_of_rates_within_each_country(self):
        # average rate must fall as the settlement gets smaller
        for country, types in LOCATIONS.items():
            avg = lambda lt: sum(final_rate(p) for p in types[lt]) / len(types[lt])
            self.assertGreater(avg("Megacity"), avg("Metropolitan"))
            self.assertGreater(avg("Metropolitan"), avg("City"))
            self.assertGreater(avg("City"), avg("Village"))

    def test_wrong_combination_is_rejected(self):
        self.assertIsNone(get_place("India", "Village", "Mumbai"))
        self.assertIsNone(get_place("Bangladesh", "Megacity", "Mumbai"))


class PricingTests(SimpleTestCase):
    def test_same_house_costs_more_in_famous_city(self):
        mumbai = estimate_price(5_000_000, "India", "Megacity", "Mumbai")["price"]
        nagpur = estimate_price(5_000_000, "India", "City", "Nagpur")["price"]
        khonoma = estimate_price(5_000_000, "India", "Village", "Khonoma")["price"]
        self.assertGreater(mumbai, nagpur)
        self.assertGreater(nagpur, khonoma)

    def test_fame_raises_price_at_equal_market_level(self):
        # Kasol (fame 8) vs Malana (fame 6) -- fame is part of the difference
        a = estimate_price(1_000_000, "India", "Village", "Kasol")
        self.assertGreater(a["fame_percent"], 0)

    def test_multiplier_formula(self):
        r = estimate_price(1_000_000, "India", "Megacity", "Mumbai")
        expected = (21000 / BASELINE_RATE) * 1.15
        self.assertAlmostEqual(r["multiplier"], expected, places=3)

    def test_indian_grouping(self):
        self.assertEqual(group_indian(28400000), "2,84,00,000")
        self.assertEqual(group_indian(999), "999")
        self.assertEqual(group_indian(123456), "1,23,456")

    def test_words(self):
        self.assertEqual(short_words(28400000), "2.84 Crore")
        self.assertEqual(short_words(450000), "4.50 Lakh")

    def test_unknown_place_raises(self):
        with self.assertRaises(ValueError):
            estimate_price(1, "India", "Village", "Mumbai")
