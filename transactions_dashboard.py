from decimal import Decimal
import manage_balance


def view_expenses(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM expense")
        rows = cur.fetchall()
        print(f"{len(rows)} rows found.\n")
        print(
            "{:<20}\t{:<10}\t{:<10}\t{:<10}".format("ID", "Title", "Category", "Price")
        )
        print("-" * 50)
        for row in rows:
            print(
                "{:<20}\t{:<10}\t{:<10}\t{:<10}".format(
                    row[0], row[1], row[2], "{:.2f}".format(row[3])
                )
            )
        cur.close()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cur.close()


def view_incomes(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM income")
        rows = cur.fetchall()
        print(f"{len(rows)} rows found.\n")
        print(
            "{:<20}\t{:<10}\t{:<10}\t{:<10}".format("ID", "Title", "Category", "Price")
        )
        print("-" * 50)
        for row in rows:
            print(
                "{:<20}\t{:<10}\t{:<10}\t{:<10}".format(
                    row[0], row[1], row[2], "{:.2f}".format(row[3])
                )
            )
        cur.close()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cur.close()


def view_expenses_by_category(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT category, SUM(price) FROM expense GROUP BY category")
        rows = cur.fetchall()
        print(f"{len(rows)} rows found.\n")
        print("{:<20}\t{:<10}".format("Category", "Total Price"))
        print("-" * 50)
        for row in rows:
            print("{:<20}\t{:<10}".format(row[0], "{:.2f}".format(float(row[1]))))
        cur.close()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cur.close()


def view_incomes_by_category(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT category, SUM(price) FROM income GROUP BY category")
        rows = cur.fetchall()
        print(f"{len(rows)} rows found.\n")
        print("{:<20}\t{:<10}".format("Category", "Total Price"))
        print("-" * 50)
        for row in rows:
            print("{:<20}\t{:<10}".format(row[0], "{:.2f}".format(float(row[1]))))
        cur.close()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cur.close()


def view_total_expenses_and_incomes(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT SUM(price) FROM expense")
        total_expenses = cur.fetchone()[0] or 0.0
        cur.execute("SELECT SUM(price) FROM income")
        total_incomes = cur.fetchone()[0] or 0.0
        print(f"\nTotal Expenses: {total_expenses:.2f}")
        print(f"Total Incomes: {total_incomes:.2f}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cur.close()


def view_edit_balance(conn):
    try:
        choice = int(input("1. View balance\n2. Update balance\nEnter your choice: "))
        if choice == 1:
            print(f"\nCurrent account balance: {manage_balance.get_current_balance(conn)}")
            input("\nPress any key to continue...")
            return
        elif choice == 2:
            amount = float(input("Enter the amount to update: "))
            manage_balance.update_balance(conn, amount)
            input("\nPress any key to continue...")
            return
        else:
            print("Please enter a valid option.")
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 2.")


def dashboard_main(conn, initial_balance):
    print("\n💵 Transaction Dashboard 💵")

    while True:
        print("\n1. View Expenses")
        print("2. View Incomes")
        print("3. View Expenses by Category")
        print("4. View Incomes by Category")
        print("5. View Total Expenses and Incomes")
        print("6. Bank Balance")
        print("7. Exit")

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                view_expenses(conn)
            elif choice == 2:
                view_incomes(conn)
            elif choice == 3:
                view_expenses_by_category(conn)
            elif choice == 4:
                view_incomes_by_category(conn)
            elif choice == 5:
                view_total_expenses_and_incomes(conn)
            elif choice == 6:
                view_edit_balance(conn)
                dashboard_main(conn, initial_balance)
            elif choice == 7:
                print("Exiting dashboard.")
                break

            else:
                print("Please enter a valid option.")

        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")
