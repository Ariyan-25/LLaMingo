from flask import Flask, render_template, request, jsonify, redirect, url_for
from ollama_api import generate_response
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            bot TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/history')
def history():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT user, bot, timestamp FROM chat ORDER BY timestamp ASC")
    history = c.fetchall()
    conn.close()
    return render_template('history.html', history=history)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    bot_response = generate_response(user_input)

    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat (user, bot) VALUES (?, ?)", (user_input, bot_response))
    conn.commit()
    conn.close()

    return jsonify({"response": bot_response})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

