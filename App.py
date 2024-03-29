from flask import Flask, request, session, redirect, url_for, render_template, flash
import sqlite3
import re 
from werkzeug.security import generate_password_hash, check_password_hash
 
app = Flask(__name__)
app.secret_key = 'secret-key'
 
conn = sqlite3.connect("duty_expert.db")
 
@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    else:
        return redirect(url_for('login'))
 
@app.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        conn.execute('SELECT * FROM users WHERE username = ?', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_rs = account['password']
            if check_password_hash(password_rs, password):
                # Create session
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                # Redirect to home
                return redirect(url_for('home'))
            else:
                # Password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist (username incorrect)
            flash('Incorrect username/password')
 
    return render_template('login.html')
  
@app.route('/register', methods=['GET', 'POST'])
def register():
 
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'fullname' in request.form and 'password' in request.form:
        fullname = request.form['fullname'] #Unit name
        username = request.form['username'] #Unit code
        password = request.form['password']
    
        hashed_password = generate_password_hash(password)
 
        #Check if account exists using MySQL
        conn.execute('SELECT * FROM users WHERE username = ?', (username,))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        else:
            # Account doesnt exists and the form data is valid, now insert new account into users table
            conn.execute("INSERT INTO users (fullname, username, password) VALUES (?, ?, ?)", (fullname, username, hashed_password))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('register.html')
   
   
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
  
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        conn.execute('SELECT * FROM users WHERE id = ?', ([session['id']], ))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))
 
if __name__ == "__main__":
    app.run(debug=True)
