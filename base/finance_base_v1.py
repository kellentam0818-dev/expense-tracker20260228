import datetime
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
    record = {
        "type": record_type,
        "amount": amount,
        "category": category,
        "description": description,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        "has_checked_in_today": False
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
            break
        elif member_id not in users:
            print("Username does not exist. Please enter a valid username.")
        elif member_id in family_members:
            print("This user is already added to the family group.")
        else:
            family_members.append(member_id)
            users[member_id]["family_group"] = family_id
            print(f"User '{member_id}' added to family group '{family_id}' successfully!")

    # Update the family group data structure with the list of family members.
    family_groups[family_id]["members"] = family_members
    return family_id


