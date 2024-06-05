from flask import request, jsonify, render_template
from app import app, db
from models import Task

@app.route('/')
def home():
    return render_template('templates/index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    tasks_list = [{'id': task.id, 'task': task.task, 'due_date': task.due_date, 'completed': task.completed} for task in tasks]
    return jsonify(tasks_list)

@app.route('/tasks', methods=['POST'])
def add_task():
    task_data = request.json
    task_text = task_data.get('task')
    due_date = task_data.get('due_date')

    if task_text:
        new_task = Task(task=task_text, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added successfully'}), 201
    return jsonify({'message': 'Task and due date are required'}), 400

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'}), 200
    return jsonify({'message': 'Invalid task ID'}), 400

@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({'message': 'Task marked as completed'}), 200
    return jsonify({'message': 'Invalid task ID'}), 400
