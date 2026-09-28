#---------------------- UPDATED: app.py with SQL Server ---------------------
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'

# --- UPDATE THESE DETAILS TO MATCH YOUR SQL SERVER ---
# This string uses Windows Authentication (Trusted_Connection=yes)
DB_CONNECTION_STRING = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=ACER-PC\\MSSQL22;"  # Replace with your server name (e.g., localhost or .\SQLEXPRESS)
    "Database=TestCollege;"     # Replace with your database name
    "Trusted_Connection=yes;"
)

# Helper function to easily open a database connection
def get_db_connection():
    return pyodbc.connect(DB_CONNECTION_STRING)

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# --- NEW: REGISTER ROUTE (To easily create a test user) ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Scramble the password securely
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            # Insert the new user into SQL Server
            cursor.execute('''
                INSERT INTO Users (username, password_hash) 
                VALUES (?, ?)
            ''', (username, hashed_password))
            conn.commit()
            return redirect(url_for('login'))
        except pyodbc.IntegrityError:
            return "Username already exists. Try another."
        finally:
            conn.close()

    return render_template('register.html')

# --- UPDATED: LOGIN ROUTE ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Fetch the user from the database
        cursor.execute("SELECT username, password_hash FROM Users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        # user[0] is username, user[1] is password_hash
        # check_password_hash verifies if the typed password matches the scrambled one
        if user and check_password_hash(user[1], password):
            session['username'] = user[0]
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password."

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



#------------------------------------Old : Session authentication with SQLite --------------------------------------------------
# import sqlite3
# from flask import Flask, render_template, request, redirect, url_for, session
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.secret_key = 'your_super_secret_key'

# # The name of the file that will be created in your VS Code folder
# DB_FILE = 'users.db'

# # --- AUTO-CREATE THE DATABASE ---
# def init_db():
#     # Connect to the file (it creates the file if it doesn't exist)
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     # Create the Users table if it's the first time running
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS Users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password_hash TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # Run the setup function before the app starts
# init_db()


# @app.route('/')
# def home():
#     if 'username' in session:
#         return redirect(url_for('dashboard'))
#     return redirect(url_for('login'))


# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
        
#         hashed_password = generate_password_hash(password)

#         conn = sqlite3.connect(DB_FILE)
#         cursor = conn.cursor()
        
#         try:
#             cursor.execute('''
#                 INSERT INTO Users (username, password_hash) 
#                 VALUES (?, ?)
#             ''', (username, hashed_password))
#             conn.commit()
#             return redirect(url_for('login'))
#         except sqlite3.IntegrityError:
#             # This triggers if the username already exists in the database
#             return "Username already exists. Try another."
#         finally:
#             conn.close()

#     return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         conn = sqlite3.connect(DB_FILE)
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT username, password_hash FROM Users WHERE username = ?", (username,))
#         user = cursor.fetchone()
#         conn.close()

#         # user[0] is username, user[1] is the hashed password
#         if user and check_password_hash(user[1], password):
#             session['username'] = user[0]
#             return redirect(url_for('dashboard'))
#         else:
#             error = "Invalid username or password."

#     return render_template('login.html', error=error)


# @app.route('/dashboard')
# def dashboard():
#     if 'username' in session:
#         return render_template('dashboard.html', username=session['username'])
#     return redirect(url_for('login'))


# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))


# if __name__ == '__main__':
#     app.run(debug=True)