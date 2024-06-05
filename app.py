from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Connect to database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="todo_list"
)

cursor = conn.cursor()

# Check if the 'tasks' table exists, if not, create it
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255), due_date VARCHAR(20), completed BOOLEAN)")
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()

    # Convert the tasks to a list of dictionaries
    tasks_list = []
    for task in tasks:
        task_dict = {
            'id': task[0],
            'task': task[1],
            'due_date': str(task[2]), 
            'completed': bool(task[3])
        }
        tasks_list.append(task_dict)

    return jsonify(tasks_list)


@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    task = task_data.get('task')
    due_date = task_data.get('due_date')

    if task and due_date:
        cursor.execute("INSERT INTO tasks (task, due_date, completed) VALUES (%s, %s, %s)", (task, due_date, False))
        conn.commit()
        return jsonify({'message': 'Task added successfully'}), 201
    return jsonify({'message': 'Task and due date are required'}), 400


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    return jsonify({'message': 'Task marked as completed'}), 200


if __name__ == '__main__':
    app.run(debug=True)
