import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
HF_TOKEN = os.getenv('HUGGING_FACE_API_KEY')

class SimpleBot:
    def __init__(self, token, hf_token):
        self.token = token
        self.hf_token = hf_token
        self.api_url = f"https://api.telegram.org/bot{token}/"
        self.hf_url = "https://api-inference.huggingface.co/models/gpt2"
        self.last_update = 0
    
    def send_message(self, chat_id, text):
        requests.post(self.api_url + "sendMessage", json={"chat_id": chat_id, "text": text})
    
    def get_ai_response(self, prompt):
        try:
            headers = {"Authorization": f"Bearer {self.hf_token}"}
            response = requests.post(self.hf_url, headers=headers, json={"inputs": prompt}, timeout=10)
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', 'Не смог ответить')[:500]
            return "Сервер занят, попробуй позже"
        except Exception as e:
            return f"Ошибка: {str(e)[:100]}"
    
    def get_updates(self):
        try:
            response = requests.get(self.api_url + "getUpdates", params={"offset": self.last_update + 1, "timeout": 30})
            return response.json().get('result', [])
        except:
            return []
    
    def handle_message(self, message):
        chat_id = message['chat']['id']
        text = message.get('text', '')
        if text.startswith('/start'):
            self.send_message(chat_id, "Привет! 👋 Я AI бот. Напиши что-нибудь и я ответу!")
        elif text.startswith('/help'):
            self.send_message(chat_id, "Просто напиши любой вопрос или текст!")
        elif text:
            response = self.get_ai_response(text)
            self.send_message(chat_id, response)
    
    def run(self):
        print("🤖 Бот запущен!")
        while True:
            try:
                updates = self.get_updates()
                for update in updates:
                    if 'message' in update:
                        self.handle_message(update['message'])
                        self.last_update = update['update_id']
                time.sleep(1)
            except Exception as e:
                print(f"Ошибка: {e}")
                time.sleep(5)

if __name__ == "__main__":
    if not TELEGRAM_TOKEN or not HF_TOKEN:
        print("❌ Ошибка: добавьте TELEGRAM_BOT_TOKEN и HUGGING_FACE_API_KEY!")
    else:
        bot = SimpleBot(TELEGRAM_TOKEN, HF_TOKEN)
        bot.run()
