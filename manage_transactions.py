from decimal import Decimal
from manage_balance import get_current_balance
import psycopg2

def add_expense(conn):
    title = input("Enter expense title: ")
    category = input("Enter expense category: ")
    price = float(input("Enter expense price: "))

    if conn is None:
        print("Database connection is not established.")
        return

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expense (title, category, price) VALUES (%s, %s, %s)",
        (title, category, price),
    )
    current_balance = get_current_balance(conn)
    new_balance = current_balance - Decimal(price)
    cur.execute(
        "INSERT INTO balance (current_balance) VALUES (%s)",
        (new_balance,),
    )
    conn.commit()
    cur.close()

    print("Expense added successfully.")


def add_income(conn):
    title = input("Enter income title: ")
    category = input("Enter income category: ")
    price = float(input("Enter income price: "))

    if conn is None:
        print("Database connection is not established.")
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO income (title, category, price) VALUES (%s, %s, %s)",
            (title, category, price),
        )
        current_balance = get_current_balance(conn)
        new_balance = current_balance + Decimal(price)
        cur.execute(
            "INSERT INTO balance (current_balance) VALUES (%s)",
            (new_balance,),
        )
        conn.commit()
    except psycopg2.errors.InFailedSqlTransaction:
        conn.rollback()
        print("Current transaction is aborted, commands ignored until end of transaction block.")
    finally:
        cur.close()

    print("Income added successfully.")


def delete_expense(conn):
    expense_id = input("ID of expense to delete: ")

    if conn is None:
        print("Database connection is not established.")
        return

    cur = conn.cursor()

    cur.execute("DELETE FROM expense WHERE id = %s", (expense_id,))
    conn.commit()
    cur.close()

    print("Expense deleted successfully.")


def delete_income(conn):
    income_id = input("ID of income to delete: ")

    if conn is None:
        print("Database connection is not established.")
        return

    cur = conn.cursor()

    cur.execute("DELETE FROM income WHERE id = %s", (income_id,))
    conn.commit()
    cur.close()

    print("Income deleted successfully.")


def manage_transactions_main(conn):
    print("\n💵 Manage transactions 💵")

    while True:
        print("\n1. Add expense.")
        print("2. Add income.")
        print("3. Delete transactions.")
        print("4. Exit.")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_expense(conn)
            elif choice == 2:
                add_income(conn)
            elif choice == 3:
                while True:
                    select = int(input("Delete [1].transaction or [2].income?"))
                    if select == 1:
                        delete_expense(conn)
                    elif select == 2:
                        delete_income(conn)
                    else:
                        print("Please enter a valid input")
            elif choice == 4:
                return
            else:
                print("Please enter a valid input")

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
