from flask import Flask, jsonify, request
from flask_cors import CORS
from database import init_db, create_chatbot, get_chatbots, update_chatbot, delete_chatbot, add_training_data, get_training_data, delete_training_data, get_chat_history, save_conversation
from chatbot_engine import ChatbotEngine
import os
app = Flask(__name__)
CORS(app)
DB_PATH = os.path.join(os.path.dirname(__file__), 'chatbot.db')
init_db(DB_PATH)
engine = ChatbotEngine()
@app.route('/api/chatbots', methods=['GET'])
def list_chatbots():
    chatbots = get_chatbots(DB_PATH)
    return jsonify(chatbots)
@app.route('/api/chatbots', methods=['POST'])
def add_chatbot():
    data = request.json
    chatbot_id = create_chatbot(DB_PATH, data['name'], data['description'], data.get('tone', 'friendly'))
    return jsonify({'id': chatbot_id, 'message': 'Chatbot created successfully'})
@app.route('/api/chatbots/<int:chatbot_id>', methods=['GET'])
def get_chatbot(chatbot_id):
    chatbots = get_chatbots(DB_PATH)
    chatbot = next((c for c in chatbots if c['id'] == chatbot_id), None)
    return jsonify(chatbot) if chatbot else jsonify({'error': 'Chatbot not found'}), 404
@app.route('/api/chatbots/<int:chatbot_id>', methods=['PUT'])
def update_chatbot_route(chatbot_id):
    data = request.json
    update_chatbot(DB_PATH, chatbot_id, data)
    return jsonify({'message': 'Chatbot updated'})
@app.route('/api/chatbots/<int:chatbot_id>', methods=['DELETE'])
def delete_chatbot_route(chatbot_id):
    delete_chatbot(DB_PATH, chatbot_id)
    return jsonify({'message': 'Chatbot deleted'})
@app.route('/api/chatbots/<int:chatbot_id>/train', methods=['POST'])
def train_chatbot(chatbot_id):
    data = request.json
    intent = data.get('intent')
    patterns = data.get('patterns', [])
    response = data.get('response')
    for pattern in patterns:
        add_training_data(DB_PATH, chatbot_id, intent, pattern, response)  
    engine.load_training_data(DB_PATH, chatbot_id)
    return jsonify({'message': 'Training data added'})
@app.route('/api/chatbots/<int:chatbot_id>/training', methods=['GET'])
def list_training(chatbot_id):
    data = get_training_data(DB_PATH, chatbot_id)
    return jsonify(data)
@app.route('/api/chatbots/<int:chatbot_id>/training/<int:training_id>', methods=['DELETE'])
def remove_training(chatbot_id, training_id):
    delete_training_data(DB_PATH, training_id)
    engine.load_training_data(DB_PATH, chatbot_id)
    return jsonify({'message': 'Training item deleted'})
@app.route('/api/chatbots/<int:chatbot_id>/chat', methods=['POST'])
def chat(chatbot_id):
    data = request.json
    user_message = data.get('message')   
    if not user_message:
        return jsonify({'error': 'Message required'}), 400   
    response = engine.get_response(chatbot_id, user_message)
    save_conversation(DB_PATH, chatbot_id, user_message, response) 
    return jsonify({'response': response})
@app.route('/api/chatbots/<int:chatbot_id>/history', methods=['GET'])
def chat_history(chatbot_id):
    history = get_chat_history(DB_PATH, chatbot_id)
    return jsonify(history)
@app.route('/api/chatbots/<int:chatbot_id>/analytics', methods=['GET'])
def get_analytics(chatbot_id):
    history = get_chat_history(DB_PATH, chatbot_id)
    total_conversations = len(history)
    return jsonify({
        'total_conversations': total_conversations,
        'total_messages': sum(len(item['messages']) for item in history) if history else 0
    })
if __name__ == '__main__':
    app.run(debug=True, port=5000)
