from flask_login import UserMixin
import random
from werkzeug.security import generate_password_hash, check_password_hash
import re

# silly user model
class User(UserMixin):
    def __init__(self, name, password):
        self.id = name
        self.name = name
        self.password = password
        
    def __repr__(self):
        return "%s/%s/%s" % (self.id, self.name, self.password)

class UserManager:
    def __init__(self, sql_conn):
        self.sql_conn = sql_conn
        
    def get(self, username, password):
        # Find user with same name
        cursor = self.sql_conn.execute('SELECT * FROM users WHERE username = ?', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            print(account)
            password_rs = account[2]
            if check_password_hash(password_rs, password):
                # Redirect to home
                return User(username, password_rs)
            else:
                # Password incorrect
                return None
        else:
            # Account doesnt exist (username incorrect)
            return None
        
        
    def get_session(self, username):
        # Find user with same name
        cursor = self.sql_conn.execute('SELECT * FROM users WHERE username = ?', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # Find user with same name
        if account:
            return User(username, "")
        else:
            return None
        
    def register(self, username, password):
        fullname = username
        hashed_password = generate_password_hash(password)
        if self.get(username, password):
            raise Exception("Username already registered")
        elif not re.match(r'[A-Za-z0-9]+', username):
            raise Exception('Username must contain only characters and numbers!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            self.sql_conn.execute("INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)", (fullname, username, hashed_password))
            self.sql_conn.commit()
        
    def delete(self, name, password):
        pass
