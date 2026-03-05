import sqlite3
from datetime import datetime

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS chatbots 
                 (id INTEGER PRIMARY KEY, name TEXT, description TEXT, tone TEXT, created_at TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS training_data 
                 (id INTEGER PRIMARY KEY, chatbot_id INTEGER, intent TEXT, pattern TEXT, response TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS conversations 
                 (id INTEGER PRIMARY KEY, chatbot_id INTEGER, user_message TEXT, bot_response TEXT, timestamp TIMESTAMP)''')
    
    conn.commit()
    conn.close()

def create_chatbot(db_path, name, description, tone='friendly'):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO chatbots (name, description, tone, created_at) VALUES (?, ?, ?, ?)',
              (name, description, tone, datetime.now()))
    conn.commit()
    chatbot_id = c.lastrowid
    conn.close()
    return chatbot_id

def get_chatbots(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, name, description, tone, created_at FROM chatbots')
    chatbots = [{'id': row[0], 'name': row[1], 'description': row[2], 'tone': row[3], 'created_at': row[4]} for row in c.fetchall()]
    conn.close()
    return chatbots

def update_chatbot(db_path, chatbot_id, data):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    name = data.get('name')
    description = data.get('description')
    tone = data.get('tone')
    
    if name:
        c.execute('UPDATE chatbots SET name = ? WHERE id = ?', (name, chatbot_id))
    if description:
        c.execute('UPDATE chatbots SET description = ? WHERE id = ?', (description, chatbot_id))
    if tone:
        c.execute('UPDATE chatbots SET tone = ? WHERE id = ?', (tone, chatbot_id))
    
    conn.commit()
    conn.close()

def delete_chatbot(db_path, chatbot_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM chatbots WHERE id = ?', (chatbot_id,))
    c.execute('DELETE FROM training_data WHERE chatbot_id = ?', (chatbot_id,))
    c.execute('DELETE FROM conversations WHERE chatbot_id = ?', (chatbot_id,))
    conn.commit()
    conn.close()

def add_training_data(db_path, chatbot_id, intent, pattern, response):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO training_data (chatbot_id, intent, pattern, response) VALUES (?, ?, ?, ?)',
              (chatbot_id, intent, pattern, response))
    conn.commit()
    conn.close()

def get_training_data(db_path, chatbot_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT id, intent, pattern, response FROM training_data WHERE chatbot_id = ?', (chatbot_id,))
    data = [{'id': row[0], 'intent': row[1], 'pattern': row[2], 'response': row[3]} for row in c.fetchall()]
    conn.close()
    return data

def delete_training_data(db_path, training_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('DELETE FROM training_data WHERE id = ?', (training_id,))
    conn.commit()
    conn.close()

def save_conversation(db_path, chatbot_id, user_message, bot_response):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO conversations (chatbot_id, user_message, bot_response, timestamp) VALUES (?, ?, ?, ?)',
              (chatbot_id, user_message, bot_response, datetime.now()))
    conn.commit()
    conn.close()

def get_chat_history(db_path, chatbot_id):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT user_message, bot_response, timestamp FROM conversations WHERE chatbot_id = ? ORDER BY timestamp', 
              (chatbot_id,))
    history = [{'user': row[0], 'bot': row[1], 'timestamp': row[2]} for row in c.fetchall()]
    conn.close()
    return history
