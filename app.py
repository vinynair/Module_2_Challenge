# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans. The application promts the user for relevant
financial 

Example:
    $ python app.py
"""

#Import required libraries:
import sys
import questionary
from pathlib import Path
import csv

#Import modular load_csv script
from qualifier.utils.fileio import load_csv

#Import modular financial calculator functions
from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

#Import filter functions from modular code files
from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

#Prompt user to enter the path of the daily rate file. Error message and system exit if incorrect path is entered.
def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)

#Function that prompts the user to enter 5 financial criteria.
def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value

#Function thata filters through the bank data vs each of the financial criteria entered. Funtion returns list of banks that the user qualifies for a loan from.
def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    
    print(f"Found {len(bank_data_filtered)} qualifying loans")
    if len(bank_data_filtered) == 0:
        sys.exit("You are not eligible for any loans from our partner banks.")
    return bank_data_filtered

    

#Function that gives the user the option to save and to enter a path name if they wish to save the results.
def save_qualifying_loans(qualifying_loans):
    action = questionary.select(
        "Do you want to save your results?", choices=["Yes", "No"]).ask()
    if action == "No":
        sys.exit(
        "OK - Will exit without saving results."
        )
    #Set output path for output file.
    else:    

        outputcsv = questionary.text(
        "Please enter the desired file name + (.csv). Type 'cancel' to cancel save").ask()
# Open the output CSV file path using `with open`
        if outputcsv == "cancel":
            sys.exit("You cancelled the save")
        else:
            with open(outputcsv, "w") as csvfile:
    # Create a csvwriter and write ech row of qualifying loan list.
                csvwriter = csv.writer(csvfile, delimiter=",")

                for loan in qualifying_loans:
                    csvwriter.writerow(loan)

def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    
    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)
    


run()
