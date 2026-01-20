from turtle import title
from flask import Flask, app, jsonify, request


todos = [
    {"id": 1, "title": "Learn REST APIs", "completed": False},
    {"id": 2, "title": "Build a Flask app", "completed": False},
    {"id": 3, "title": "Test with Postman", "completed": False}
]

app = Flask(__name__)

def get_next_id():
    if not todos:
        return 1
    else:
        return todos[-1]['id'] + 1

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify({'todos': todos}), 200

@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_single_todo(todo_id):
    for data in todos:
        if data['id'] == todo_id:
            todo = data
            return jsonify(todo), 200
        else:
            return jsonify({'error': "Todo not found"}), 404

@app.route('/todos', methods=['POST'])
def post_todo():
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
        
    new_todo = {
        "id" : get_next_id(),
        "title": request.json["title"],
        "completed" : request.json["completed"]
    }
    todos.append(new_todo)
    return jsonify(new_todo, 201)

@app.route('/')
def welcome():
    return jsonify("Welcome to my First Api")


if __name__ == '__main__':
    app.run(debug=True, port=5000)