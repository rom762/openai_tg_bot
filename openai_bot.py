import logging
from telegram.ext import (CommandHandler, MessageHandler, ApplicationBuilder,
                          filters, ConversationHandler)
from openai import OpenAI
import settings
import yt_dlp as youtube_dl
from youtube_dwnld import download_mp3
from anketa import anketa_start, second_cat, final_step
from make_image import get_image_filename

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG)

client = OpenAI(api_key=settings.api_key)


async def start(update, context):
    context.chat_data.clear()
    await update.message.reply_text('Hi! I am your AI bot. Ask me anything!')


async def send_audio(update, context):
    user_request = ' '.join(context.args).strip()
    logging.debug(user_request)
    filename = download_mp3(user_request)

    with open(filename, 'rb') as af:
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=af)


async def handle_message(update, context):

    await context.bot.send_chat_action(chat_id=update.effective_chat.id,
                                       action='typing')
    message = update.message.text
    logging.info(f'User message:{message}')
    if "https://www.youtube.com" in message:
        await context.bot.send_message(update.effective_chat.id, "Please wait...")
        video_info = youtube_dl.YoutubeDL().extract_info(url=message, download=False)
        filename = f"{video_info['title']}.mp3"
        options = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename,
        }
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([video_info['webpage_url']])

        logging.info("Download complete... {}".format(filename))
        await context.bot.send_audio(chat_id=update.effective_chat.id, audio=open(filename, 'rb'))
    else:
        messages = context.chat_data.get('messages', [])
        messages.append({"role": "user", "content": message})
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "system",
                "content": "You are a helpful assistant."}, ] + messages
        )

        bot_response = response.choices[0].message.content
        messages.append({"role": "assistant", "content": bot_response})
        context.chat_data['messages'] = messages

        tokens = response.usage.total_tokens 
        logging.debug(f"current response tokens: {tokens}")

        if 'total_tokens' not in context.chat_data:
            context.chat_data['total_tokens'] = tokens
        else:
            context.chat_data['total_tokens'] += tokens

        await update.message.reply_text(bot_response)


async def stats(update, context):
    messages = context.chat_data.get('messages', [])
    tokens = context.chat_data.get('total_tokens', 0)
    text = f"messages: {len(messages)}\ntokens: {tokens}"
    await update.message.reply_text(text)


def main():
    application = ApplicationBuilder().token(settings.telegram_bot_token).build()

    anketa = ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^(мемас с котами)$'), anketa_start)
        ],
        states={
            "second_cat": [MessageHandler(filters.TEXT, second_cat)],
            "final": [MessageHandler(filters.TEXT, final_step)]
        },
        fallbacks=[]
    )

    application.add_handler(anketa)
    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler(["stats",], stats))
    application.add_handler(CommandHandler(["file", "music"], send_audio))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                           handle_message))
    application.run_polling()


if __name__ == '__main__':
    main()
