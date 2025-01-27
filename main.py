# Create a program tom manage daily expenses, manage them, and calculate weekly totals

from db_connection import connect_to_db
from manage_transactions import manage_transactions_main
from transactions_dashboard import dashboard_main
from manage_balance import get_current_balance


def run_a_query(conn):
    cur = conn.cursor()
    cur.execute(
        "ALTER TABLE expense ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"
    )
    print("Query executed successfully.")


def main(conn):
    print("\n\nYour daily expense tracker")
    initial_balance = get_current_balance(conn)
    print(f"\n💵 Current balance: {initial_balance}")

    print("\n1. Manage transactions.")
    print("2. Open Dashboard.")
    print("3. Exit.")
    try:
        choice = int(input("Enter your choice: "))

        while True:
            if choice == 1:
                manage_transactions_main(conn)
                main(conn)
                continue
            elif choice == 2:
                dashboard_main(conn, initial_balance)
                main(conn)
                continue
            elif choice == 3:
                break
            else:
                print("Please enter a valid option")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")


if __name__ == "__main__":
    conn = connect_to_db()
    if conn:
        main(conn)
