import unittest

from mortgage import (
    effective_monthly_rate,
    calculate_emi,
    amortization_schedule,
    calculate_payoff_duration,
)


class TestMortgageCalculator(unittest.TestCase):

    def test_monthly_rate(self):
        self.assertAlmostEqual(
            effective_monthly_rate(12, "monthly"),
            0.01,
        )

    def test_zero_interest_emi(self):
        self.assertAlmostEqual(
            calculate_emi(120000, 0, 10),
            1000,
        )

    def test_emi_is_positive(self):
        emi = calculate_emi(1000000, 8.5, 20)
        self.assertGreater(emi, 0)

    def test_compounding_methods(self):
        methods = ["monthly", "weekly", "daily", "continuous"]

        rates = [
            effective_monthly_rate(8.5, method)
            for method in methods
        ]

        self.assertEqual(len(rates), 4)
        self.assertTrue(all(rate > 0 for rate in rates))

    def test_schedule_pays_off_loan(self):
        schedule = amortization_schedule(120000, 0, 10)

        self.assertEqual(len(schedule), 120)
        self.assertAlmostEqual(
            schedule[-1]["balance"], 0, places=5
        )

    def test_schedule_has_principal_and_interest(self):
        schedule = amortization_schedule(100000, 12, 1)

        self.assertGreater(schedule[0]["interest"], 0)
        self.assertGreater(schedule[0]["principal"], 0)
        self.assertAlmostEqual(
            schedule[-1]["balance"], 0, places=5
        )

    def test_custom_payoff_duration(self):
        months = calculate_payoff_duration(
            120000, 0, 10000
        )
        self.assertEqual(months, 12)

    def test_payment_too_small(self):
        with self.assertRaises(ValueError):
            calculate_payoff_duration(100000, 12, 500)

    def test_invalid_loan_amount(self):
        with self.assertRaises(ValueError):
            calculate_emi(0, 8, 20)

    def test_invalid_compounding(self):
        with self.assertRaises(ValueError):
            effective_monthly_rate(8, "yearly")


if __name__ == "__main__":
    unittest.main()
