from services.expense_service import analyze_expenses
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <file_path>")
        return

    file_path = sys.argv[1]

    result = analyze_expenses(file_path)
    print("Result :- ", result)
    if result is None:
        return

    print(f"Total: ₹{result['total']}")
    for cat, amt in result['category_breakdown'].items():
        print(f"{cat}: ₹{amt}")
    print(f"Top Category: {result['top_category']}")


if __name__ == "__main__":
    main()