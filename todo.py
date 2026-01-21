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
    # request is from user (postman) and is given in json 
    if not request.json or 'title' not in request.json:
        return jsonify({"error": "Title is required"}), 400
        
    new_todo = {
        "id" : get_next_id(),
        "title": request.json["title"],
        "completed" : request.json["completed"]
    }
    todos.append(new_todo)
    return jsonify(new_todo, 201)

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    for i in todos:
        if i['id'] == todo_id:
            todo = i

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404
    
    if not request.json:
        return jsonify({'error': 'Request must be JSON'}), 404

    todo['title'] = request.json.get('title', todo['title'])
    todo['completed'] = request.json.get('completed', todo['completed'])

    return jsonify(todo), 200


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    for i in todos:
        if i['id'] == todo_id:
            todo = i

    if todo is None:
        return jsonify({'error': 'Todo not found'}), 404

    todos.remove(todo)
    return jsonify({'message': "Todo deleted successfully"}), 200

@app.route('/')
def welcome():
    return jsonify({"message": "Welcome to Todo API",
                    "endpoints": {
                        "GET /todos": "Get all todos",
                        "GET /todos/<id>": "Get a specific todo",
                        "POST /todos": "Create a new todo",
                        "PUT /todos/<id>": "Update a todo",
                        "DELETE /todos/<id>": "Delete a todo"
                    }})

if __name__ == '__main__':
    app.run(debug=True, port=5000)