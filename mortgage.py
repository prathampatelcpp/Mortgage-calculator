
import math


def effective_monthly_rate(annual_rate, compounding):
    """Convert nominal annual interest into an effective monthly rate."""
    if annual_rate < 0:
        raise ValueError("Annual interest rate cannot be negative.")

    j = annual_rate / 100

    if compounding == "monthly":
        return j / 12

    if compounding == "weekly":
        return (1 + j / 52) ** (52 / 12) - 1

    if compounding == "daily":
        return (1 + j / 365) ** (365 / 12) - 1

    if compounding == "continuous":
        return math.expm1(j / 12)

    raise ValueError("Unsupported compounding method.")


def calculate_emi(principal, annual_rate, years, compounding="monthly"):
    """Calculate the fixed monthly payment for a mortgage."""
    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero.")
    if years <= 0:
        raise ValueError("Loan term must be greater than zero.")

    months = round(years * 12)
    if months < 1:
        raise ValueError("Loan term must be at least one month.")

    rate = effective_monthly_rate(annual_rate, compounding)

    if rate == 0:
        return principal / months

    factor = math.expm1(months * math.log1p(rate))
    return principal * rate * (factor + 1) / factor


def amortization_schedule(
    principal, annual_rate, years, compounding="monthly"
):
    """Return one repayment record per month."""
    payment = calculate_emi(
        principal, annual_rate, years, compounding
    )
    rate = effective_monthly_rate(annual_rate, compounding)
    balance = principal
    schedule = []
    total_interest = 0.0

    months = round(years * 12)

    for month in range(1, months + 1):
        interest = balance * rate
        principal_paid = payment - interest

        # Avoid a negative balance caused by the final payment.
        actual_payment = min(payment, balance + interest)
        principal_paid = actual_payment - interest
        balance = max(0.0, balance - principal_paid)
        total_interest += interest

        schedule.append({
            "month": month,
            "payment": actual_payment,
            "principal": principal_paid,
            "interest": interest,
            "balance": balance,
        })

        if balance < 0.000001:
            balance = 0.0
            schedule[-1]["balance"] = balance
            break

    return schedule


def calculate_payoff_duration(principal, annual_rate, monthly_payment, compounding="monthly"):
    """Return the number of months needed to repay the loan."""
    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero.")
    if monthly_payment <= 0:
        raise ValueError("Monthly payment must be greater than zero.")

    rate = effective_monthly_rate(annual_rate, compounding)

    if rate > 0 and monthly_payment <= principal * rate:
        raise ValueError(
            "Payment must exceed the first month's interest."
        )

    balance = principal
    months = 0
    max_months = 1200  # Maximum 100 years

    while balance > 0.000001 and months < max_months:
        interest = balance * rate
        actual_payment = min(monthly_payment, balance + interest)
        balance = max(0.0, balance + interest - actual_payment)
        months += 1

    if balance > 0.000001:
        raise ValueError("Loan could not be repaid within 100 years.")

    return months
