import datetime as dt
from collections import defaultdict

# === Core data structure ===
# User Dictionary: {User ID: {name: Username, type: "single"/"family", family_group: Family Group ID, records: [], has_checked_in_today: Checked in today or not}}
users = {}

# Family group dictionary: {Family group ID: {name: Family name, members: [User ID1, User ID2]}}
family_groups = {}

# financial categories
INCOME_CATEGORIES = ["Salary", "Part-time", "Rent income", "Stock profit", "Other" ]
EXPENSE_CATEGORIES = ["Food", "Transportation", "Utilities", "Education", "Entertainment", "Other"]

# Encapsulate common functions
# Function 1: Add imcome or expense record
def add_record(user_id, record_type, amount, category, description):
    # Check if the record type is valid (income or expense)
    if user_id not in users:
        return False, f"User {user_id} does not exist."
    # Check if the record type is valid (income or expense)
    if record_type not in ["income", "expense"]:
        return False, "Invalid record type. Must be 'income' or 'expense'."
    # Check if the category is valid based on the record type
    target_categories = INCOME_CATEGORIES if record_type == "income" else EXPENSE_CATEGORIES
    if category not in target_categories:
        return False, f"Invalid category for {record_type}. Valid categories: {', '.join(target_categories)}."
    
    record = {
        "type": record_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users[user_id]["records"].append(record)
    return True, "Record added successfully."

# Function 2: Regular financial calculation and summary
def calculate_finance(user_ids):
    # Initialize totals
    total_income = 0
    total_expense = 0

    # Iterate through all the passed user IDs (individual user/multiple family members) 
    # and calculate the total income and total expenditure.
    for user_id in user_ids:
        # Iterate through the financial records of each user and accumulate the totals based on the record type (income or expense).
        if user_id not in users:
            continue  # Skip if user does not exist
        for record in users[user_id]["records"]:
            # Check the type and accumulate the amount accordingly.
            if record["type"] == "income":
                total_income += record["amount"]
            elif record["type"] == "expense":
                total_expense += record["amount"]
    
    # Calculate the surplus (total income - total expenditure)
    surplus = total_income - total_expense
    # Return the calculated totals (total income, total expenditure, and surplus) to be used for generating financial summaries and reports.
    return total_income, total_expense, surplus

# Public function: Extract the repeated logic of revenue and expenditure (amount verification + note acquisition)
def _input_amount_and_note(record_type):
    """
    Private public function that encapsulates amount input validation and remark retrieval
    :param record_type: record type income/expense
    :return: validated amount (float), remark (str)
    """
    # Amount input validation
    while True:
        amount_input = input(f"Enter the {record_type} amount (positive number): ")
        # Verify that the format is valid & the value is valid
        if amount_input.replace('.', '', 1).isdigit() and float(amount_input) > 0:
            amount = float(amount_input)
            amount = round(amount, 2)  # Round to 2 decimal places
            break
        else:
            print(f"Invalid input. Please enter a positive number for the {record_type} amount.")

    note = input(f"Enter a note for this {record_type} (optional): ").strip()
    note = note if note else "No note provided"
    return amount, note

# Public function: Select according to the record type (income/expense)
def _select_category(record_type):
    """
    Private public function that encapsulates category selection based on record type
    :param record_type: record type income/expense
    :return: selected category (str)
    """
    target_categories = INCOME_CATEGORIES if record_type == "income" else EXPENSE_CATEGORIES
    while True:
        print(f"Select a category for this {record_type}:")
        for idx, category in enumerate(target_categories, 1):
            print(f"{idx}. {category}")
        category_input = input("Enter the number corresponding to the category: ").strip()
        if category_input.isdigit() and 1 <= int(category_input) <= len(target_categories):
            return target_categories[int(category_input) - 1]
        else:
            print("Invalid input. Please enter a valid number corresponding to the category.")

# Individual user Registration
def register_user():
    print("\nWelcome to **Online Finance Secretary**!")
    while True:
        user_id = input("Please create your unique username: ").strip()
        if user_id in users:
            print("Username already exists. Please choose a different username.")
        elif not user_id:
            print("Username cannot be empty. Please enter a valid username.")
        else:
            break
    # Initialize the user data structure with the provided username and default values for other fields.
    users[user_id] = {
        "name": user_id,
        "type": "single",
        "family_group": None,
        "records": [],
        "has_checked_in_today": False,
        "daily_budget": None
    }
    print(f"Individual account '{user_id}' created successfully!")
    return user_id

# Family group Registration
def register_family_group():
    print("\nWelcome to **Online Finance Secretary**!")
    print("💡 Tip: Note: Family groups are optional – only create one if you need to share finances with others.")
    while True:
        family_id = input("Please create your unique family group name: ").strip()
        if family_id in family_groups:
            print("Family group name already exists. Please choose a different name.")
        elif not family_id:
            print("Family group name cannot be empty. Please enter a valid name.")
        else:
            break
    # Initialize the family group data structure with the provided family group name and default values for other fields.
    family_groups[family_id] = {"name": family_id, "members": []}
    print(f"Family group '{family_id}' created successfully!")
    
    # Add family members to the family group (must be registered users)
    family_members = []
    print("\nPlease add family members to the family group. Enter 'done' when finished.")
    while True:
        member_id = input("Enter a username to add to the family group (or 'done' to finish): ").strip()
        if member_id.lower() == 'done':
            # Add 1 member to the family group at least
            if len(family_members) == 0:
                print("Error! Please add at least one member to the family group.")
                continue
            else:
                print(f"Finished adding family members to the family group '{family_id}'.")
                break
        elif member_id not in users:
            print("Username does not exist. Please enter a valid username.")
        elif member_id in family_members:
            print("This user is already added to the family group.")
        else:
            family_members.append(member_id)
            users[member_id]["family_group"] = family_id
            users[member_id]["type"] = "family"
            print(f"User '{member_id}' added to family group '{family_id}' successfully!")

    # Update the family group data structure with the list of family members.
    family_groups[family_id]["members"] = family_members
    return family_id

# Universal submenu function: Handles the logic for "return to main menu/continue operation"
# Parameter description:
# - operation_name: Current operation name (such as "expense"/"income"), used for prompt text
# Return value: True = continue operation, False = return to main menu
def show_operation_submenu(operation_name):
    while True:
        print(f"\n{operation_name.capitalize()} Menu:")
        print("1. Return to main menu")
        print(f"2. Continue {operation_name}")
        sub_choice = input("Enter the number corresponding to your choice(1 or 2): ").strip()
        if sub_choice == '1':
            return False
        elif sub_choice == '2':
            return True
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Get today's date (format: 2026-03-04) for check-in/daily consumption statistics
def get_current_date():
    today = dt.date.today()
    return today.strftime("%Y-%m-%d")

today_str = get_current_date()

# Check-in function and simulated check-in record list
def check_in(user_id):
    while True:
    # Verify if the user exists
        if user_id not in users:
            print(f"Error: User '{user_id}' does not exist!")
            return   
        today = get_current_date()
        if not users[user_id]["has_checked_in_today"]:
            users[user_id]["has_checked_in_today"] = True
            print(f"✅ {user_id} checked in successfully for {today}!")
        else:
            print(f"ℹ️ {user_id} already checked in for {today}.")

        # Check in the submenu and manually select to return/continue to the main menu.
        continue_flag = show_operation_submenu("check-in")
        if not continue_flag:
            return

# === Set daily budget function ===
def set_daily_budget(user_id):
    if user_id not in users:
        print(f"Error: User '{user_id}' does not exist!")
        return
    while True:
        budget_input = input("Please enter your daily budget (positive number): ")
        if not budget_input.replace('.', '', 1).isdigit():
            print("Invalid input. Please enter a positive number for the daily budget.")
            continue
        daily_budget = float(budget_input)
        daily_budget = round(daily_budget, 2)
        if daily_budget <= 0:
            print("The budget must be greater than 0. Please enter a valid number!")
            continue
        # The budget is stored in the user's dictionary.
        users[user_id]["daily_budget"] = daily_budget
        print(f"✅ Daily budget set to: ${daily_budget} for user '{user_id}'!")
        return daily_budget


# === Add expense ===
def add_expense(user_id):
        while True:
            print("\n===== Add New Expense =====")
            # Call public function: Get amount + remarks
            amount, note = _input_amount_and_note("expense")
            # Call public function: Select expense category
            category = _select_category("expense")
            # Call core function: Add record
            success, msg = add_record(user_id, "expense", amount, category, note)
            print(msg)
            # Call the submenu function to decide whether to return to the main menu or continue adding expenses.
            continue_flag = show_operation_submenu("expense")
            if not continue_flag:
                return
        # Select option 2 to automatically return to the beginning of the loop and continue adding expenses


# === Add income (Call public functions and associate users) ===
def add_income(user_id):
    while True:
        print("\n===== Add New Income =====")
        # Call public function: Get amount + remarks
        amount, note = _input_amount_and_note("income")
        # Call public function: Select income category
        category = _select_category("income")
        # Call core function: Add record
        success, msg = add_record(user_id, "income", amount, category, note)
        print(msg)
        continue_flag = show_operation_submenu("income")
        if not continue_flag:
            return

# === View financial summary (Call core function and associate users) ===
# General Dispatch Desk: main function
def main():
    current_user = None
    print("="*50)
    print("Welcome to the Financial Tracker!")
    print("="*50)

    # 1. Sign in or sign up
    while True:
        print("\nPlease select an option:")
        print("1.Register as an individual user")
        print("2.Sign in")        
        choice = input("Enter the number corresponding to your choice: ").strip()
        if choice == '1':
            current_user = register_user()
            break
        elif choice == '2':
            user_id = input("Enter your username to sign in: ").strip()
            if user_id in users:
                current_user = user_id
                print(f"Welcome back, {current_user}!")
                break
            else:
                print("Username does not exist. Please try again or sign up.")
        else:
            print("Invalid choice. Please enter 1 or 2.")

    # 2. Main menu loop(Execute in a loop until the user chooses to exit.)
    while True:
        print("\n" + "="*50)
        print(f"Current User: {current_user} | User Type: {users[current_user]['type']} | Date: {today_str}")
        print("="*50)
        print("\nMain Menu:")
        print("1. Check-in")
        print("2. Set Daily Budget")
        print("3. Add Expense")
        print("4. Add Income")
        print("5. View Financial Summary")
        print("6. Create and set family financial group (if needed).")
        print("7. Exit")
        choice = input("Enter the number corresponding to your choice: ").strip()

        # Call the corresponding function based on the user's choice. 
        # For family users, when viewing the financial summary, calculate the total income and total expenditure for all family members and display the overall financial summary for the family group. For individual users, calculate and display only their own financial summary.
        if choice == '1':
            check_in(current_user)
        elif choice == '2':
            set_daily_budget(current_user)
        elif choice == '3':
            add_expense(current_user)
        elif choice == '4':
            add_income(current_user)
        elif choice == '5':
            # For family users, calculate finance for all family members; for individual users, calculate only for themselves.
            if users[current_user]["type"] == "family":
                family_id = users[current_user]["family_group"]
                family_members = family_groups[family_id]["members"]
                total_income, total_expense, surplus = calculate_finance(family_members)
                print(f"\nFinancial Summary for Family Group '{family_groups[family_id]['name']}':")
            else:
                total_income, total_expense, surplus = calculate_finance([current_user])
                print(f"\nFinancial Summary for User '{current_user}':")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: ${total_expense:.2f}")
            print(f"Surplus: ${surplus:.2f}")
        elif choice == '6':
            family_id = register_family_group()
            print(f"User type updated to 'family' and associated with the family group {family_id} successfully!")
        elif choice == '7':
            print("Thank you for using the Financial Tracker! Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")

# Run the main function to start the program
if __name__ == "__main__":
    main()
