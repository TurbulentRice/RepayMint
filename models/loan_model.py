import mysql.connector

class LoanModel:
  def __init__(self, host, user, password, database):
    self.conn = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database
    )
    self.cursor = self.conn.cursor()

  def create_loan(self, user_id, start_balance, interest_rate, payment_amount, title, term):
    self.cursor.execute("""
      INSERT INTO loans (user_id, start_balance, interest_rate, payment_amount, title, term)
      VALUES (%s, %s, %s, %s, %s, %s)
    """, (user_id, start_balance, interest_rate, payment_amount, title, term))
    self.conn.commit()

  def get_user_loans(self, user_id):
    self.cursor.execute("""
      SELECT start_balance, interest_rate, payment_amount, title, term
      FROM loans
      WHERE user_id = %s
    """, (user_id,))
    return self.cursor.fetchall()

  def close_connection(self):
    self.cursor.close()
    self.conn.close()
