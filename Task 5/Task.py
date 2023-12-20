#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from flask import Flask, request, jsonify

app = Flask(__name__)


todos = []


def find_todo_by_id(todo_id):
    for todo in todos:
        if todo['id'] == todo_id:
            return todo
    return None


@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = find_todo_by_id(todo_id)
    if todo:
        return jsonify(todo), 200
    else:
        return jsonify({"message": "Todo not found"}), 404


@app.route('/todos', methods=['GET'])
def get_all_todos():
    return jsonify(todos), 200


@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    if 'title' in data and 'description' in data:
        new_id = len(todos) + 1
        new_todo = {'id': new_id, 'title': data['title'], 'description': data['description']}
        todos.append(new_todo)
        return jsonify({"message": "Todo created successfully"}), 201
    else:
        return jsonify({"message": "Invalid request data"}), 400


@app.route('/todos/<int:todo_id>', methods=['PATCH'])
def update_todo(todo_id):
    data = request.json
    todo = find_todo_by_id(todo_id)
    if todo:
        if 'title' in data:
            todo['title'] = data['title']
        if 'description' in data:
            todo['description'] = data['description']
        return jsonify({"message": "Todo updated successfully"}), 200
    else:
        return jsonify({"message": "Todo not found"}), 404


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = find_todo_by_id(todo_id)
    if todo:
        todos.remove(todo)
        return jsonify({"message": "Todo deleted successfully"}), 200
    else:
        return jsonify({"message": "Todo not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)



