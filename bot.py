import os
import requests

class TelegramAI:
    def __init__(self, token, model):
        self.token = token
        self.model = model
        self.api_url = f'https://api.telegram.org/bot{self.token}/'
        self.huggingface_api_url = 'https://api-inference.huggingface.co/models/' + model

    def send_message(self, chat_id, text):
        requests.post(self.api_url + 'sendMessage', data={'chat_id': chat_id, 'text': text})

    def generate_response(self, prompt):
        headers = {'Authorization': f'Bearer {os.getenv("HUGGINGFACE_API_TOKEN")}' }
        response = requests.post(self.huggingface_api_url, headers=headers, json={'inputs': prompt})
        return response.json()[0]['generated_text']

    def handle_update(self, update):
        chat_id = update['message']['chat']['id']
        user_message = update['message']['text']
        bot_response = self.generate_response(user_message)
        self.send_message(chat_id, bot_response)

    def run(self):
        offset = None
        while True:
            updates = requests.get(self.api_url + 'getUpdates', params={'offset': offset}).json()
            for update in updates['result']:
                self.handle_update(update)
                offset = update['update_id'] + 1

# To run the bot
# if __name__ == '__main__':
#     bot = TelegramAI('YOUR_TELEGRAM_BOT_TOKEN', 'YOUR_HUGGINGFACE_MODEL')
#     bot.run()