# Updated bot.py code

class LightweightBot:
    def __init__(self, token):
        self.token = token
        self.commands = {}

    def add_command(self, command, handler):
        self.commands[command] = handler

    def handle_command(self, command, *args):
        if command in self.commands:
            return self.commands[command](*args)
        else:
            return 'Command not found!'

    def run(self):
        # Bot running logic goes here
        pass

# This is where you'd initialize the bot
if __name__ == '__main__':
    bot = LightweightBot(token='YOUR_TOKEN_HERE')
    # Example command
    bot.add_command('greet', lambda name: f'Hello, {name}')
    print(bot.handle_command('greet', 'User'))