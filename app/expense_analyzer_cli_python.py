import sys
import csv

# Load all the expenses in the list
def load_expenses(file_path):
    list_of_expenses = []
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            list_of_expenses.append({'category': row['category'].strip(), 'amount': int(row['amount'])})
    return list_of_expenses

# Calculate toatl expense
def calculate_totals(expenses):
    return sum(expense['amount'] for expense in expenses)

# Group by category all the expenses
def group_by_category(expenses):
    grouped_expense = {}
    for expense in expenses:
        grouped_expense[expense['category']] = grouped_expense.get(expense['category'], 0) + expense['amount']
    return grouped_expense

# Get the top category
def get_top_category(grouped_expenses):
    return max(grouped_expenses, key=grouped_expenses.get)

def main():
    file_path = sys.argv[1]
    list_of_expenses = load_expenses(file_path)
    total_expenses = calculate_totals(list_of_expenses)
    grouped_expenses = group_by_category(list_of_expenses)
    top_category = get_top_category(grouped_expenses)

    print(f"Total Expenses: ₹{total_expenses}")
    for cat, amount in grouped_expenses.items():
        print(f"{cat}: ₹{amount}")
    print(f"Top Category: {top_category}")

main()
