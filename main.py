import configparser
import logging
import os
import telegram
from flask import Flask, request
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler

# # Load data from config.ini file
# config = configparser.ConfigParser()
# config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# # Initial bot by Telegram access token
# bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))
bot = telegram.Bot(token = str(os.getenv("TELEGRAM_BOT_TOKEN")))

@app.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


def reply_handler(bot, update):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="你好，歡迎使用這個機器人！")



# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))
dispatcher.add_handler(CommandHandler('start', start))


if __name__ == "__main__":
    # Running server
    app.run(debug=True)









# # 定義處理 /start 指令的函式
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text('歡迎使用本機器人！')

# # 定義處理 /help 指令的函式
# async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     message = '/start - 開始使用本機器人\n' \
#               '/help - 獲取幫助\n' \
#               '/subscribe - 訂閱 BTC 價格提醒\n' \
#               '/unsubscribe - 取消訂閱 BTC 價格提醒'
#     await update.message.reply_text(message)

# # 定義處理 /subscribe 指令的函式
# async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     # 將用戶加入訂閱列表
#     user_id = update.effective_user.id
#     if user_id not in subscribers:
#         subscribers.append(user_id)
#         await update.message.reply_text('您已成功訂閱 BTC 價格提醒！')
#     else:
#         await update.message.reply_text('您已訂閱 BTC 價格提醒！')

# # 定義處理 /unsubscribe 指令的函式
# async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     # 將用戶從訂閱列表中刪除
#     user_id = update.effective_user.id
#     if user_id in subscribers:
#         subscribers.remove(user_id)
#         await update.message.reply_text('您已成功取消訂閱 BTC 價格提醒！')
#     else:
#         await update.message.reply_text('您尚未訂閱 BTC 價格提醒！')

# # 定義處理 BTC 價格提醒的函式
# async def btc_price_alert() -> None:
#     while True:
#         price = get_kline()
#         if int(float(price[1])) >= 26900:
#             for user in subscribers:
#                 await app.bot.send_message(chat_id=user, text='BTC 現價已達到 27000！')
#             break
#         await asyncio.sleep(10)


# app = ApplicationBuilder().token("6058955159:AAHPinHT7IWkIPQJNpeN1-4pL2qddNy8W-w").build()

# # 註冊 /start, /help, /subscribe 和 /unsubscribe 指令的處理函式
# app.add_handler(CommandHandler('start', start))
# app.add_handler(CommandHandler('help', help))
# app.add_handler(CommandHandler('subscribe', subscribe))
# app.add_handler(CommandHandler('unsubscribe',unsubscribe))


# subscribers = []

# asyncio.ensure_future(btc_price_alert())

# app.run_polling()
