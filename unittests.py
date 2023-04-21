#Import necessary modules
import unittest
import sqlite3
#Import functions from ExpenseTracker module
from ExpenceTracker import add_expense, view_expenses, create_table

#Define test cases as a subclass of unittest.TestCase
class ExpenseTrackerTests(unittest.TestCase):
    # Setup method to create an in-memory database and add test data to the expenses table
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        create_table(self.conn)
        
        self.test_expenses = [
            ('2022-01-01', 'Groceries', 50.0, 'Food'),
            ('2022-01-02', 'Gas', 30.0, 'Transportation'),
            ('2022-01-03', 'Movie tickets', 25.0, 'Entertainment')
        ]
        
        cursor = self.conn.cursor()
        cursor.executemany("INSERT INTO expenses (date, description, amount, category) VALUES (?, ?, ?, ?)", self.test_expenses)
        self.conn.commit()
        
    # Teardown method to close the database connection
    def tearDown(self):
        self.conn.close()
        
    def test_add_expense(self):
        # test adding a valid expense
        add_expense(self.conn, '2022-01-04', 'Coffee', 5.0, 'Food')
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE description = 'Coffee'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        
        # test adding an invalid expense (negative amount)
        with self.assertRaises(ValueError):
            add_expense(self.conn, '2022-01-05', 'Gift', -20.0, 'Gifts')
        
    def test_view_expenses(self):
        # test viewing all expenses
        expected_output = '\n'.join([f"{row[0]} {row[1]} {row[2]} {row[3]}" for row in self.test_expenses])
        self.assertEqual(view_expenses(self.conn), expected_output)
        
        # test viewing expenses sorted by date
        expected_output = '\n'.join([f"{row[0]} {row[1]} {row[2]} {row[3]}" for row in sorted(self.test_expenses, key=lambda x: x[0])])
        self.assertEqual(view_expenses(self.conn, sort_by='date'), expected_output)
        
        # test viewing expenses filtered by category
        expected_output = '\n'.join([f"{row[0]} {row[1]} {row[2]} {row[3]}" for row in self.test_expenses if row[3] == 'Food'])
        self.assertEqual(view_expenses(self.conn, category='Food'), expected_output)