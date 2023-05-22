from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configure MySQL connection
mysql_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='todo'
)

cursor = mysql_connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT,
        completed BOOLEAN NOT NULL DEFAULT 0
    )
''')

@app.route('/')
def index():
    cursor = mysql_connection.cursor()
    cursor.execute('SELECT * FROM todos')
    todos = cursor.fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    description = request.form['description']
    cursor = mysql_connection.cursor()
    cursor.execute('INSERT INTO todos (title, description) VALUES (%s, %s)', (title, description))
    mysql_connection.commit()
    return redirect('/')

@app.route('/toggle/<int:todo_id>')
def toggle(todo_id):
    cursor = mysql_connection.cursor()
    cursor.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
    todo = cursor.fetchone()
    completed = not todo[3]
    cursor.execute('UPDATE todos SET completed = %s WHERE id = %s', (completed, todo_id))
    mysql_connection.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
