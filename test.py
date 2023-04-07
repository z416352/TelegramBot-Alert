import os
import logging
import configparser
from flask import Flask, request

import telegram
from telegram import Update
from telegram.ext import Updater, Filters, CallbackContext
from telegram.ext import MessageHandler, CommandHandler


# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# 設定 bot token 和 webhook URL
TOKEN = config['TELEGRAM']['ACCESS_TOKEN']
WEBHOOK_URL = config['TELEGRAM']['WEBHOOK_URL']


# 創建 Flask 應用程序對象
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)


# 定義 /start 指令處理函式
def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat.id, text="歡迎使用本機器人！")

# 定義 /help 指令處理函式
def help(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat.id, text="這是一個 Telegram Bot，支援以下指令：\n\n/start - 開始使用\n/help - 獲取幫助\n/info - 獲取信息")

# 定義 /info 指令處理函式
def info(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat.id, text="這是一個 Telegram Bot 程式，使用 python-telegram-bot 套件版本 13.15。")

def reply_handler(update: Update, context: CallbackContext):
    """Reply message."""
    if update.message:
        context.bot.send_message(chat_id=update.message.chat.id, text=update.message.text)


# def message_handler(update: Update, context: CallbackContext):
#     context.bot.send_message(chat_id=update.message.chat.id, text=update.message.text)

# def start(update: Update, context: CallbackContext):  # New
#     context.bot.send_message(
#         chat_id=update.message.chat.id, text="Hello")

# 定義 webhook 接收請求的路由
@app.route('/callback', methods=['POST'])
def webhook():
    # 從 POST 請求中解析更新
    update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
    # 將更新傳遞給調度器進行處理
    updater.dispatcher.process_update(update)
    # 回應 OK 狀態碼
    return 'OK'

# def webhook(request):
#     update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
#     chat_id = update.message.chat_id
#     text = update.message.text
#     context = CallbackContext(dispatcher=updater.dispatcher, job_queue=None, chat_data={}, user_data={})
#     context.bot.send_message(chat_id=chat_id, text=text)


updater = Updater(TOKEN)
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))
updater.dispatcher.add_handler(CommandHandler("start", callback=start))
updater.dispatcher.add_handler(CommandHandler("help", callback=help))
updater.dispatcher.add_handler(CommandHandler("info", callback=info))

if __name__ == "__main__":
    # updater.start_polling()
    # updater.idle()
    # updater.stop()

    updater.start_webhook(
        listen = "127.0.0.1",
        port = 8443,
        url_path = "callback",
        webhook_url = WEBHOOK_URL
    ) 

    app.run()
