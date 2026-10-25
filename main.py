
from mortgage import (
    calculate_emi,
    calculate_payoff_duration,
    amortization_schedule,
)

COMPOUNDING_OPTIONS = {
    "1": ("Monthly", "monthly"),
    "2": ("Weekly", "weekly"),
    "3": ("Daily", "daily"),
    "4": ("Continuous", "continuous"),
}


def format_inr(amount):
    """Format a number using Indian digit grouping."""
    value = f"{amount:.2f}"
    integer, decimal = value.split(".")

    if len(integer) > 3:
        last_three = integer[-3:]
        remaining = integer[:-3]
        groups = []

        while remaining:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]

        integer = ",".join(groups + [last_three])

    return f"₹{integer}.{decimal}"


def get_number(prompt, allow_zero=False):
    while True:
        try:
            value = float(input(prompt))

            if value < 0 or (value == 0 and not allow_zero):
                print("Please enter a valid positive number.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a number.")


def get_compounding():
    print("\nChoose compounding interval:")
    for key, (label, _) in COMPOUNDING_OPTIONS.items():
        print(f"{key}. {label}")

    while True:
        choice = input("Enter choice (1-4): ").strip()
        if choice in COMPOUNDING_OPTIONS:
            return COMPOUNDING_OPTIONS[choice]
        print("Invalid choice. Select a number from 1 to 4.")


def display_summary(principal, payment, schedule):
    total_paid = sum(row["payment"] for row in schedule)
    total_interest = sum(row["interest"] for row in schedule)
    months = len(schedule)

    print("\n" + "=" * 45)
    print("         MORTGAGE CALCULATION")
    print("=" * 45)
    print(f"Loan amount       : {format_inr(principal)}")
    print(f"Monthly EMI       : {format_inr(payment)}")
    print(f"Repayment period  : {months} months "
          f"({months // 12} years, {months % 12} months)")
    print(f"Total interest    : {format_inr(total_interest)}")
    print(f"Total repayment   : {format_inr(total_paid)}")
    print("=" * 45)


def display_schedule(schedule):
    print("\nAMORTIZATION SCHEDULE")
    print("-" * 91)
    print(
        f"{'Month':>5} {'Payment':>13} {'Principal':>13} "
        f"{'Interest':>13} {'Balance':>15}"
    )
    print("-" * 91)

    for row in schedule:
        print(
            f"{row['month']:>5} "
            f"{format_inr(row['payment']):>13} "
            f"{format_inr(row['principal']):>13} "
            f"{format_inr(row['interest']):>13} "
            f"{format_inr(row['balance']):>15}"
        )


def calculate_mortgage():
    principal = get_number("Enter loan amount (₹): ")
    annual_rate = get_number("Enter annual interest rate (%): ", True)
    years = get_number("Enter loan term (years): ")

    label, compounding = get_compounding()

    emi = calculate_emi(
        principal, annual_rate, years, compounding
    )
    schedule = amortization_schedule(
        principal, annual_rate, years, compounding
    )

    print(f"\nCompounding method: {label}")
    display_summary(principal, emi, schedule)

    choice = input(
        "\nDisplay full amortization schedule? (y/n): "
    ).strip().lower()

    if choice == "y":
        display_schedule(schedule)


def calculate_custom_payoff():
    principal = get_number("Enter outstanding loan amount (₹): ")
    annual_rate = get_number("Enter annual interest rate (%): ", True)
    payment = get_number("Enter your monthly payment (₹): ")

    label, compounding = get_compounding()

    months = calculate_payoff_duration(
        principal, annual_rate, payment, compounding
    )

    print(f"\nCompounding method: {label}")
    print(f"Monthly payment: {format_inr(payment)}")
    print(f"Payoff duration: {months} months")
    print(f"               {months // 12} years "
          f"and {months % 12} months")


def main():
    while True:
        print("\n====== MORTGAGE CALCULATOR ======")
        print("1. Calculate EMI and amortization schedule")
        print("2. Calculate payoff duration for a chosen payment")
        print("3. Exit")

        choice = input("Choose an option (1-3): ").strip()

        try:
            if choice == "1":
                calculate_mortgage()
            elif choice == "2":
                calculate_custom_payoff()
            elif choice == "3":
                print("Thank you for using Mortgage Calculator!")
                break
            else:
                print("Invalid option. Please select 1, 2, or 3.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
