import csv
import sqlite3

def add_expense(conn):
    """
    Adds a new expense to the expenses table in the database.

    Parameters:
    conn (sqlite3.Connection): The database connection.

    Returns:
    None
    """
    # Prompt the user to enter the expense details
    date = input("Enter the date (YYYY-MM-DD): ")
    description = input("Enter a description: ")
    
    #Validate user input for expense amount
    while True:
        try:
            amount = float(input("Enter the amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    category = input("Enter the category: ")

    # Insert the expense into the database
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (date, description, amount, category) VALUES (?, ?, ?, ?)", (date, description, amount, category))
    conn.commit()
    
    #Inform the user that the expense has been added successfully
    print("Expense added successfully.")
    
def view_expenses(conn, sort_by=None, category=None, output_file=None):
    """
    Writes the expenses in the expenses table in the database to a CSV file.

    Parameters:
    conn (sqlite3.Connection): The database connection.
    sort_by (str): The column to sort the expenses by (date or category).
    category (str): The category to filter the expenses by.
    output_file (str): The name of the output CSV file. If not specified, the
        expenses will be written to a file named "expenses.csv" in the current
        directory.

    Returns:
    None
    """
    cursor = conn.cursor()
    query = "SELECT * FROM expenses"
    
    # If a category is specified, add a WHERE clause to the query to filter by that category
    if category:
        query += f" WHERE category = '{category}'"
        
    # If sort_by is 'date', sort the expenses by date (ascending order)
    # If sort_by is 'category', sort the expenses by category (ascending order)
    if sort_by == 'date':
        query += " ORDER BY date ASC"
    elif sort_by == 'category':
        query += " ORDER BY category ASC"
        
    # Execute the query and fetch all rows
    cursor.execute(query)
    rows = cursor.fetchall()
    
    # If no rows are returned, print a message and return None
    if not rows:
        print("No expenses found.")
        return
    
    # If output_file is not specified, use the default filename 'expenses.csv'
    if output_file is None:
        output_file = "expenses.csv"
    
    # Write the expenses to the output CSV file
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Description", "Amount", "Category"])
        for row in rows:
            writer.writerow(row)
    
    # Prints a message that expenses have been written to a CSV file
    print(f"Expenses written to {output_file}.")



    #This loop runs indefinitely until the user decides to exit the program by choosing the 'Exit' option from the main menu.
    while True:
    
        # If the user selects the 'View expenses' option from the main menu:
        if choice == 2:
            
            # The user is prompted to enter how they would like to sort the expenses (by date or category) or to view without sorting.
            sort_by = input("Sort by date or category? (Enter 'date' or 'category', or press Enter to view without sorting): ")
            
            # The user is prompted to enter a category to filter by or to view all categories.
            category = input("Enter a category to filter by (or press Enter to view all categories): ")
            
            # The user is prompted to enter a filename to save the expenses as a CSV file or to skip.
            output_file = input("Enter a filename to save the expenses as a CSV file (or press Enter to skip): ")
            
            # The view_expenses() function is called with the sort_by, category, and output_file arguments passed in.
            view_expenses(conn, sort_by, category, output_file)
    
    
    
def create_table(conn):
    """
    Creates the expenses table in the database (if it doesn't already exist).

    Parameters:
    conn (sqlite3.Connection): The database connection.

    Returns:
    None
    """
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS expenses (date TEXT, description TEXT, amount REAL, category TEXT)")
    conn.commit()
    
# Connect to the database and create the expenses table if necessary
conn = sqlite3.connect('expenses.db')
create_table(conn)

# Display main menu and prompt user for input until they choose to exit
while True:
    
     # Print the main menu
    print("\nExpense Tracker")
    print("1. Add new expense")
    print("2. View all expenses")
    print("3. Exit")
    
    try:
        choice = int(input("Enter your choice (1-3): "))
    except ValueError:
        print("Invalid choice. Please enter a number between 1 and 3.")
        continue
    
    # Check the user's choice and execute the corresponding function
    if choice == 1:
        add_expense(conn)
    elif choice == 2:

        # Ask the user for sorting and filtering options
        sort_by = input("Sort by date or category? (Enter 'date' or 'category', or press Enter to view without sorting): ")
        category = input("Enter a category to filter by (or press Enter to view all categories): ")
        
        # Retrieve the expenses and print them to the console
        expenses = view_expenses(conn, sort_by, category)
        
        if not expenses:
            # If no expenses were found, print a message to inform the user
            print("No expenses found.")
        else:
            # If expenses were found, print a table with the expenses
            print("\nDate        Description                     Amount     Category")
            print("-----------------------------------------------------------------")
            for expense in expenses:
                # Format each expense as a row in the table
                print(f"{expense[0]}  {expense[1]:30} ${expense[2]:<8.2f}  {expense[3]}")
    elif choice == 3:
        # If the user chooses to exit, print a message and break the loop
        print("Exiting...")
        break
    else:
        # If an invalid choice is entered, print an error message and continue the loop
        print("Invalid choice. Please enter a number between 1 and 3.")