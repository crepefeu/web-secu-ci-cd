#!/usr/bin/env python3
"""
Vulnerable Web Application for CI/CD Security Testing
This application contains intentional vulnerabilities for educational purposes.
"""

import os
import sqlite3
import subprocess
from flask import Flask, request, render_template_string, send_file

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
    
    # Insert some test data
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (1, 'admin', 'password123', 'admin@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, username, password, email) VALUES (2, 'user', 'secret456', 'user@example.com')")
    
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template_string("""
    <h1>Vulnerable Web Application</h1>
    <p>This application contains vulnerabilities for testing purposes.</p>
    <ul>
        <li><a href="/login">SQL Injection Login</a></li>
        <li><a href="/file">Path Traversal File Read</a></li>
        <li><a href="/ping">Command Injection</a></li>
    </ul>
    """)

# Vulnerable SQL Injection endpoint
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        # VULNERABILITY: SQL Injection
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return f"Welcome {user[1]}! Your email is: {user[3]}"
            else:
                return "Invalid credentials"
        except Exception as e:
            return f"Database error: {str(e)}"
    
    return render_template_string("""
    <h2>Login</h2>
    <form method="post">
        Username: <input type="text" name="username"><br><br>
        Password: <input type="password" name="password"><br><br>
        <input type="submit" value="Login">
    </form>
    <p>Try: admin' OR '1'='1' --</p>
    """)

# Vulnerable Path Traversal endpoint
@app.route('/file')
def read_file():
    filename = request.args.get('filename', 'README.md')
    
    # VULNERABILITY: Path Traversal
    try:
        file_path = os.path.join('.', filename)
        return send_file(file_path)
    except Exception as e:
        return f"Error reading file: {str(e)}"

# Vulnerable Command Injection endpoint
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    
    # VULNERABILITY: Command Injection
    try:
        result = subprocess.check_output(f'ping -c 1 {host}', shell=True, text=True)
        return f"<pre>{result}</pre>"
    except Exception as e:
        return f"Ping failed: {str(e)}"

# Simple math function for testing
def add_numbers(a, b):
    """Add two numbers together."""
    return a + b

def multiply_numbers(a, b):
    """Multiply two numbers together."""
    return a * b

def divide_numbers(a, b):
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)