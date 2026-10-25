# Mortgage Calculator

A Python-based command-line Mortgage Calculator that calculates monthly EMI, total interest, total repayment, and loan payoff duration.

## Features

- Calculate monthly EMI based on loan amount, annual interest rate, and loan term.
- Support monthly, weekly, daily, and continuous interest compounding.
- Generate a month-by-month amortization schedule.
- Calculate loan payoff duration based on a chosen monthly payment.
- Display amounts in Indian Rupee (INR) format.
- Validate user inputs and handle calculation errors.
- Include automated unit tests using Python's `unittest` framework.

## Technologies Used

- Python
- Math module
- Unittest
- Git and GitHub

## Project Structure

```text
Mortgage-Calculator/
├── main.py
├── mortgage.py
├── test_mortgage.py
├── README.md
└── .gitignore
```

## How to Run

1. Install Python 3 if it is not already installed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run the application:

```bash
python main.py
```

## Run the Tests

Execute the following command in the project directory:

```bash
python -m unittest -v
```

## Concepts Practiced

- Functions and modular programming
- Input validation and exception handling
- Loops and conditional statements
- Mathematical calculations and financial formulas
- Lists and dictionaries
- Automated unit testing
- Version control using Git and GitHub

## Disclaimer

This project is intended for educational purposes. Actual loan calculations may vary depending on lender policies, compounding conventions, fees, and repayment terms.
