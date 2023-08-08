from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, CallbackContext

from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

TOKEN = os.getenv("BOT_TOKEN")

# States for tracking user responses
START, WAITING_FOR_QUESTION, ANSWER_YES, ANSWER_NO, ANSWER_DONT_KNOW = range(5)


def start(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton(
            "Start Poll", callback_data=str(WAITING_FOR_QUESTION))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        "Welcome to the magic quiz! Press 'Start Poll' to begin.", reply_markup=reply_markup)
    return START


def show_question(update: Update, context: CallbackContext) -> int:
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="yes"),
         InlineKeyboardButton("No", callback_data="no"),
         InlineKeyboardButton("I don't know", callback_data="dont_know")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Are you a magician?", reply_markup=reply_markup)
    return WAITING_FOR_QUESTION


def poll_callback(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    answer = query.data
    response = get_response_text(answer)
    query.message.reply_text(response)

    return ConversationHandler.END


def handle_text(update: Update, context: CallbackContext) -> int:
    text = update.message.text
    user_id = update.effective_user.id
    state = context.user_data.get('state', None)

    if context.user_data == 'how are you?':
        update.message.reply_text("Great! Now, what's new in your life?")
        context.user_data['state'] = None
    elif context.user_data == 'Are you single?':
        update.message.reply_text("No way!")
        context.user_data['state'] = None
    elif context.user_data == 'How is the weather today?':
        update.message.reply_text("Sunny, thanks!")
        context.user_data['state'] = None
    else:
        update.message.reply_text("Don't know how to respond to that")
        context.user_data['state'] = None

    return ConversationHandler.END


def get_response_text(answer: str) -> str:
    if answer == "yes":
        return "Yes, indeed! You're a magician!"
    elif answer == "no":
        return "That's okay! Not everyone is a magician."
    elif answer == "dont_know":
        return "No worries! It's always good to be curious."


def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("poll", start)],
        states={
            START: [CallbackQueryHandler(start)],
            WAITING_FOR_QUESTION: [CallbackQueryHandler(show_question)],
            ANSWER_YES: [CallbackQueryHandler(poll_callback)],
            ANSWER_NO: [CallbackQueryHandler(poll_callback)],
            ANSWER_DONT_KNOW: [CallbackQueryHandler(poll_callback)]
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conversation_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
