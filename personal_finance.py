from typing import Any


from unittest import result
from flask import Flask, jsonify, request, app
import sqlite3, datetime

app = Flask(__name__)

# database using sqlite3
db = "finance.db"
def init_db():
    conn = sqlite3.connect(db)
    curs = conn.cursor()

    curs.execute("""
    CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
    amount REAL NOT NULL CHECK(amount > 0),
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    created_at TEXT NOT NULL)
    """)

    conn.commit()
    conn.close()

    print("Database initialized")


def get_db():
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row #to get row access
    return conn

init_db()

#ROUTES AND ENDPOINTs
@app.route("/")
def get_home():
    return jsonify({
        "message": "Personal Finance Tracker API - SQLite3 Version",
        "endpoints": {
            "POST /transactions": "Add a transaction",
            "GET /transactions": "Get all transactions",
            "GET /transactions/<id>": "Get single transaction",
            "DELETE /transactions/<id>": "Delete transaction",
            "GET /balance": "Get current balance",
            "GET /summary": "Get financial summary",
            "GET /spending-by-category": "Get spending grouped by category"
        }})

@app.route("/transactions", methods=["POST"])
def create_trans():
    data = request.json
    if not data:
        return jsonify({"error": "No data in request"}), 400

    if "type" not in data or data["type"] not in ['income', 'expense']:
        return jsonify({"error": "Type must be 'income' or 'expense'"}), 400

    if "amount" not in data or data['amount'] <= 0:
        return jsonify({"error": "Amount must be positive"}), 400

    if not data["category"]:
        return jsonify({"error": "Amount must be positive"}), 400

    if "date" not in data:
        return jsonify({"error": "No date provided"}), 400

    created = datetime.datetime.now().isoformat()

    conn = get_db()
    curs = conn.cursor()

    curs.execute("""
    INSERT INTO transactions(type, amount, category, description, date, created_at)
    VALUES (?,?,?,?,?,?)""", (data['type'], data['amount'], data['category'], data['description'], data['date'], created))

    conn.commit()
    trans_id = curs.lastrowid
    conn.close()

    return jsonify({"id" : trans_id, "message": "Transaction success"}), 201


@app.route("/transactions", methods=["GET"])
def  get_trans():

    trans_type = request.args.get('type')
    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db()

    query = 'SELECT * FROM transactions WHERE 1=1'
    params = []

    if trans_type:
        query += 'AND type = ?'
        params.append(trans_type)
    
    if category:
        query += 'AND type = ?'
        params.append(category)
    
    if start_date:
        query += 'AND type = ?'
        params.append(start_date)
    
    if end_date:
        query += 'AND type = ?'
        params.append(end_date)
    
    transactions = conn.execute(query, params).fetchall()
    conn.close()
    result = [dict(t) for t in transactions]
    return jsonify({"transactions": result}), 200


@app.route("/transations/ <int:id>", methods=["DELETE"])
def delete_trans(id):
    conn = sqlite3.connect(db)
    curs= conn.cursor()

    curs.execute("""DELETE FROM transactions WHERE id = ?""", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Transaction deleted successfully"})