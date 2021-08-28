# Vintech Loan Corp #
# Loan Qualifier Application #
---
The loan qualifier application compares a user's financial data to a list of bank loan criteria, and returns a list of bank's that the user meets the loan criteria for. The user is prompted to enter the location of the daily rate bank file and their financial information, the application filters the bank loan criteria against the user's financial data, the application returns a list of compatible banks, and allows the user to save this list as a local .csv file.

## Technologies

The following libraries are imported in the application. Please ensure system compability. The questionary library must be installed prior to running.
Imports:
1) sys
2) questionary
3) pathlib
4) csv

---

## Installation Guide

1) Install questionary.
2) Please note that the daily_rate_sheet.csv, qualifier.filters folder, qualifier.utils folder must be saved in the root directory.


---

## Usage

1) Run app.py in the Command Line Interface.
2) When prompted for the file path for the rate sheet, please enter 'daily_rate_sheet.csv' without the quotations.
3) When prompted for a file name, plese save as a csv file by ending the file name in '.csv' without the quotations.
4) You may choose to not save results and exit the application.
5) If you do not qualify for any loans, the application will not save results and exit.

---

## Contributors ##

Contributors:
University of Washington

Contact Information:
vn392@stern.nyu.edu

---

## License
MIT 
GitHub
VS Terminal
