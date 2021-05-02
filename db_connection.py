import mysql.connector as mySQL
from loan import *

#   Context Manager for Cursor
class Cursor:
    def __init__(self, connection_: mySQL.MySQLConnection):
        self.temp_cursor = connection_.cursor()

    def __enter__(self):
        return self.temp_cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.temp_cursor.close()

#   Class for loan_calc_db connection
#   Uses MySQLConnection object
#   To Do: Include imports in init, error handling wihtin object creation?
class LoanDBConnector:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "passwd": "password123",
            "database": "loan_calc_db"
        }

        #   We'll use the MySQLConnection object, so that the connection itself can be passed
        self.connection = mySQL.MySQLConnection(**self.config)

    #   Put loan object info into db
    def add_loan_to_db(self, loan_obj: StandardLoan):
        insert = "INSERT INTO loans (title, start_bal, int_rate, payment_amount) VALUES (%s, %s, %s, %s)"
        values = (loan_obj.title, loan_obj.start_balance, loan_obj.int_rate, loan_obj.payment_amt)

        with Cursor(self.connection) as c:
            c.execute(insert, values)
            self.connection.commit()

    #   Compare loan object payment history with payment history in db associated with loan obj
    #   Update payment history in db
    def add_payment_to_history(self, loan_obj: StandardLoan):
        insert = "INSERT INTO payment_history (title, start_bal, int_rate) VALUES (%s, %s, %s)"
        pass

    #   Select loans with NAME in them, return name and IDs for display in infobox
    def load_loan(self):
        pass

    def remove_loan(self, id_no):
        pass

    def wipe_db(self):
        with Cursor(self.connection) as c:
            c.execute("""SET FOREIGN_KEY_CHECKS = 0;
            TRUNCATE loans;
            TRUNCATE payment_history;
            SET FOREIGN_KEY_CHECKS = 1;
            """, multi="TRUE")

        print("DB Wiped")

    def get_loans(self):
        with Cursor(self.connection) as c:
            c.execute("SELECT * FROM loans")
            _list = [entry for entry in c]
        return _list

    #   Return payment history dict for specified loan
    def get_history_for(self, id):
        pass

    def show_tables(self):
        with Cursor(self.connection) as c:
            c.execute("SHOW TABLES")
            for table in c:
                print(table)

    def close_connection(self):
        self.connection.close()



