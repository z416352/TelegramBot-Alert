# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes

# import sqlite3

# # 定義對話的狀態
# NAME, EMAIL = range(2)

# # 定義處理/start指令的函式
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     # 回覆一則訊息
#     await update.message.reply_text('歡迎使用本機器人！請輸入 /help 以查看可用的指令。')



# def start_add_info(update: Update, context: dict):
#     # 回覆使用者，開始一個新的對話
#     update.message.reply_text('請輸入你的名字：')

#     # 設置下一步對話的狀態
#     return NAME

# def add_name(update: Update, context: dict):
#     # 取得使用者輸入的名字
#     name = update.message.text

#     # 將名字存入 context 中，以便下一步對話使用
#     context['name'] = name

#     # 回覆使用者，詢問電子郵件地址
#     update.message.reply_text('請輸入你的電子郵件地址：')

#     # 設置下一步對話的狀態
#     return EMAIL

# def add_email(update: Update, context: dict):
#     # 取得使用者輸入的電子郵件地址
#     email = update.message.text

#     # 將資料儲存到 SQLite 資料庫中
#     # conn = sqlite3.connect('data.db')
#     # c = conn.cursor()
#     # c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (context['name'], email))
#     # conn.commit()
#     # conn.close()

#     # 回覆使用者，對話結束
#     update.message.reply_text('資料已儲存，謝謝！  name = ', context['name'], 'email = ', email)

#     # 結束對話
#     return ConversationHandler.END

# def cancel(update: Update, context: dict):
#     # 回覆使用者，對話已取消
#     update.message.reply_text('對話已取消')

#     # 結束對話
#     return ConversationHandler.END


# app = ApplicationBuilder().token("6058955159:AAHPinHT7IWkIPQJNpeN1-4pL2qddNy8W-w").build()

# # 建立/start指令的處理器
# start_handler = CommandHandler('start', start)

# conv_handler = ConversationHandler(
#     entry_points=[CommandHandler('add_info', start_add_info)],
#     states={
#         NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
#         EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_email)]
#     },
#     fallbacks=[CommandHandler('cancel', cancel)]
# )


# app.add_handler(start_handler)
# app.add_handler(conv_handler)

# app.run_polling


import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# 定義對話的狀態
NAME, EMAIL = range(2)


# 定義處理/start指令的函式
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 回覆一則訊息
    await update.message.reply_text('歡迎使用本機器人！請輸入 /help 以查看可用的指令。')


# 定義處理/help指令的函式
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 回覆一則訊息，列出可用的指令
    message = '/start - 開始使用本機器人\n/add_info - 新增一條資訊'
    await update.message.reply_text(message)


# 定義處理/add_info指令的函式
async def add_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 獲取使用者傳來的資訊
    info = update.message.text

    # 回覆一則訊息
    await update.message.reply_text(f'已新增一筆資訊：{info}')


async def start_add_info(update: Update, context: dict):
    # 回覆使用者，開始一個新的對話
    await update.message.reply_text('請輸入你的名字：')

    # 設置下一步對話的狀態
    return NAME

async def add_name(update: Update, context: dict):
    # 取得使用者輸入的名字
    name = update.message.text

    # 將名字存入 context 中，以便下一步對話使用
    context['name'] = name

    # 回覆使用者，詢問電子郵件地址
    await update.message.reply_text('請輸入你的電子郵件地址：')

    # 設置下一步對話的狀態
    return EMAIL

async def add_email(update: Update, context: dict):
    # 取得使用者輸入的電子郵件地址
    email = update.message.text

    # 將資料儲存到 SQLite 資料庫中
    # conn = sqlite3.connect('data.db')
    # c = conn.cursor()
    # c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (context['name'], email))
    # conn.commit()
    # conn.close()

    # 回覆使用者，對話結束
    await update.message.reply_text('資料已儲存，謝謝！  name = ', context['name'], 'email = ', email)

    # 結束對話
    return ConversationHandler.END

async def cancel(update: Update, context: dict):
    # 回覆使用者，對話已取消
    await update.message.reply_text('對話已取消')

    # 結束對話
    return ConversationHandler.END

# 建立應用程序
app = ApplicationBuilder().token('6058955159:AAHPinHT7IWkIPQJNpeN1-4pL2qddNy8W-w').build()

# 建立/start指令的處理器
start_handler = CommandHandler('start', start)

# 建立/help指令的處理器
help_handler = CommandHandler('help', help)

# 建立/add_info指令的處理器
add_info_handler = CommandHandler('add_info', add_info)

# 建立資訊輸入的處理器
# message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, add_info)


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add_info_test', start_add_info)],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_email)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# 將處理器添加到應用程序
app.add_handler(start_handler)
app.add_handler(help_handler)
app.add_handler(add_info_handler)
# app.add_handler(message_handler)
app.add_handler(conv_handler)

# 啟動應用程序
app.run_polling()
