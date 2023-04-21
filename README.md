This project is a simple command-line application that allows users to track their expenses. It stores expenses in an SQLite database and allows the user to add new expenses or view existing expenses.

The command-line application displays a main menu with three options:

Add new expense
View all expenses
Exit
If the user selects "Add new expense", they are prompted to enter the details of the new expense (date, description, amount, and category), which are then added to the expenses table in the SQLite database.

If the user selects "View all expenses", they are prompted to specify sorting and filtering options (sort by date or category, filter by category) and optionally specify a file to save the expenses as a CSV file. The expenses are then fetched from the SQLite database, sorted and filtered as specified, and written to a CSV file.

The code defines three functions:

add_expense: This function prompts the user to enter details of a new expense and inserts it into the expenses table in the SQLite database.

view_expenses: This function fetches expenses from the expenses table in the SQLite database, sorts and filters them as specified by the user, and writes them to a CSV file.

create_table: This function creates the expenses table in the SQLite database if it doesn't already exist.

The main program starts by creating a connection to the expenses.db SQLite database and creating the expenses table if it doesn't already exist. It then displays the main menu and prompts the user to select an option. Depending on the user's selection, the appropriate function is called to perform the necessary action. This process repeats until the user selects "Exit" from the main menu.
