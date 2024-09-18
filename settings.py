from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('OPENAI_TOKEN')
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

if __name__ == "__main__":
    print(f'OPENAI_API_KEY:{api_key}')
    print(f'telegram bot token:{telegram_bot_token}')
