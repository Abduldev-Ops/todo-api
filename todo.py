from flask import Flask, app, jsonify, request


todos = [
    {"id": 1, "title": "Learn REST APIs", "completed": False},
    {"id": 2, "title": "Build a Flask app", "completed": False},
    {"id": 3, "title": "Test with Postman", "completed": False}
]

app = Flask(__name__)

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

# @app.route('/todos', methods=['POST'])
# def post_todo():
#     if request.json

@app.route('/')
def welcome():
    return jsonify("Welcome to my First Api")


if __name__ == '__main__':
    app.run(debug=True, port=5000)