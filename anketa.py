from telegram import ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from make_image import get_image_filename


async def anketa_start(update, contex):
    await update.message.reply_text(
        "Введите фразу первого кота.",
        reply_markup=ReplyKeyboardRemove()
    )
    return "second_cat"


async def second_cat(update, context):
    first_cat = update.message.text
    print(f'first_cat: {first_cat}')
    context.user_data['anketa'] = {'first_cat': first_cat}
    await update.message.reply_text('Введите фразу второго кота')
    return "final"


async def final_step(update, context):
    first = context.user_data['anketa']['first_cat']
    second = update.message.text
    filename = get_image_filename(first, second)
    with open(filename, 'rb') as af:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=filename)

    return ConversationHandler.END
