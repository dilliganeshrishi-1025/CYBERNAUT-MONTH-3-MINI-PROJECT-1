from database import get_training_data
import difflib

class ChatbotEngine:
    def __init__(self):
        self.training_data = {}
    
    def load_training_data(self, db_path, chatbot_id):
        data = get_training_data(db_path, chatbot_id)
        self.training_data[chatbot_id] = {item['intent']: {'patterns': [], 'responses': []} for item in data}
        
        for item in data:
            intent = item['intent']
            if intent not in self.training_data[chatbot_id]:
                self.training_data[chatbot_id][intent] = {'patterns': [], 'responses': []}
            
            if item['pattern'].lower() not in self.training_data[chatbot_id][intent]['patterns']:
                self.training_data[chatbot_id][intent]['patterns'].append(item['pattern'].lower())
            
            if item['response'] not in self.training_data[chatbot_id][intent]['responses']:
                self.training_data[chatbot_id][intent]['responses'].append(item['response'])
    
    def get_response(self, chatbot_id, user_input):
        if chatbot_id not in self.training_data or not self.training_data[chatbot_id]:
            return "I'm not trained yet. Please add training data first."
        
        user_input_lower = user_input.lower()
        best_intent = None
        best_match_ratio = 0
        
        for intent, data in self.training_data[chatbot_id].items():
            for pattern in data['patterns']:
                ratio = difflib.SequenceMatcher(None, user_input_lower, pattern).ratio()
                if ratio > best_match_ratio:
                    best_match_ratio = ratio
                    best_intent = intent
        
        if best_match_ratio > 0.4 and best_intent:
            responses = self.training_data[chatbot_id][best_intent]['responses']
            return responses[0] if responses else "I understand but don't have a response prepared."
        
        return "I didn't quite understand that. Can you rephrase?"
