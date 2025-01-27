from decimal import Decimal


def get_current_balance(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT current_balance FROM balance ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        return row[0] if row else 0.0

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cur.close()

    return 0.0

def update_balance(conn, new_amount):
    try:
        # Get the current balance
        current_amount = get_current_balance(conn)
        cur = conn.cursor()
        
        # Calculate the adjustment amount
        adjustment = Decimal(new_amount) - Decimal(current_amount)
        
        if adjustment > 0:
            # Record the positive adjustment in the income table
            cur.execute(
                "INSERT INTO income (title, category, price) VALUES (%s, %s, %s)",
                ("Balance Adjustment", "Adjustment", adjustment),
            )
        elif adjustment < 0:
            # Record the negative adjustment in the expense table
            cur.execute(
                "INSERT INTO expense (title, category, price) VALUES (%s, %s, %s)",
                ("Balance Adjustment", "Adjustment", abs(adjustment)),
            )
        
        # Update the balance table
        cur.execute("INSERT INTO balance (current_balance) VALUES (%s)", (Decimal(new_amount),))
        
        # Commit the changes
        conn.commit()
        print("Balance updated successfully.")
    
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cur.close()
