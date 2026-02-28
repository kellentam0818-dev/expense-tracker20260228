# Simple Expense Tracker
import datetime
#import matplotlib.pyplot as plt
#from collections import defaultdict

# 1. Get today's date (format: 2026-02-25) for check-in/daily consumption statistics
def get_current_date():
    today = datetime.date.today()
    return today.strftime("%Y-%m-%d")

today_str = get_current_date()
print(f"Today's date: {today_str}")

# Check-in function and simulated check-in record list
checkin_records = []

def check_in():
    today = get_current_date()
    if today not in checkin_records:
        checkin_records.append(today)
        print(f"Checked in for {today}!")
    else:
        print(f"Already checked in for {today}.")

# # test check-in
# check_in()
# check_in()  # Attempt to check in again on the same day

# 2. Initialize an empty list to store expenses
expense_records = []

def set_daily_budget():
    """Let the user set a daily budget and return a valid positive integer budget value."""
    while True:
        budget_input = input("Please enter your daily budget (positive integer): ")
        if budget_input.isdigit() and int(budget_input) > 0:
            daily_budget = int(budget_input)
            print(f"Daily budget set to: {budget_input}")
            return budget_input
    
        elif budget_input.isdigit():
            print(f"The budget cannot be 0. Please enter an integer greater than 0!")
             
        else:
            print("Invalid input. Please enter a positive integer for the daily budget.")

print("=== Start setting daily budget ===")
# Key step: Call the function to initialize the budget
DAILY_BUDGET = set_daily_budget()
print(f"=== Budget set successfully: {DAILY_BUDGET} ===") 

# 3. Function to add an expense

expense_records = []

def add_expense():
    while True:
        amount_input = input("Enter the expense amount (positive number): ")
        # Verify that the format is valid & the value is valid
        if amount_input.replace('.', '', 1).isdigit() and float(amount_input) > 0:
            amount = float(amount_input)
            break
        else:
            print("Invalid input. Please enter a positive number for the expense amount.")
