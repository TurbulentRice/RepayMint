import bcrypt
import mysql.connector

class UserModel:
  def __init__(self, host, user, password, database):
    self.conn = mysql.connector.connect(
      host=host,
      user=user,
      password=password,
      database=database
    )
    self.cursor = self.conn.cursor()

  def register_user(self, username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    self.cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    self.conn.commit()

  def verify_login(self, username, password):
    self.cursor.execute("SELECT user_id, username, password FROM users WHERE username = %s", (username,))
    result = self.cursor.fetchone()
    
    if result:
      user_id, username, hashed_password = result
      return user_id, username, bcrypt.checkpw(password.encode('utf-8'), bytes(hashed_password, encoding='utf-8'))
    else:
      return None, None, False
  
  def get_user_by_id(self, user_id):
    self.cursor.execute("SELECT user_id, username FROM users WHERE user_id = %s", (user_id,))
    result = self.cursor.fetchone()

    if result:
      user_id, username = result
      return {'user_id': user_id, 'username': username}
    else:
      return None
  
  def get_user_by_username(self, username):
    self.cursor.execute("SELECT user_id, username FROM users WHERE username = %s", (username,))
    result = self.cursor.fetchone()

    if result:
      user_id, username = result
      return {'user_id': user_id, 'username': username}
    else:
      return None

  def close_connection(self):
    self.cursor.close()
    self.conn.close()
