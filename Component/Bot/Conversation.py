from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext, CommandHandler, MessageHandler, Filters


NAME, PHONE = range(2)

def conversation(update, context):
    update.message.reply_text(
        '請輸入您的姓名：\n（或輸入 /cancel 取消）'
        )

    return NAME

def get_name(update, context):
    user = update.message.from_user
    context.user_data['name'] = update.message.text
    reply_keyboard = [['Cancel']]
    update.message.reply_text(
        '請輸入您的電話號碼：\n（或輸入 /cancel 取消）')
    
    return PHONE

def get_phone(update, context):
    # user = update.message.from_user
    context.user_data['phone'] = update.message.text
    update.message.reply_text(
        "謝謝您的填寫！\n"
        f"姓名：{context.user_data['name']}\n"
        f"電話：{context.user_data['phone']}"
    )
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text(
        '已取消輸入，請重新開始。\n'
        '輸入 /conversation 開始新的表單填寫'
    )
    return ConversationHandler.END

# 創建 ConversationHandler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('conversation', conversation)],
    states={
        NAME: [MessageHandler(Filters.regex('^(?!Cancel).*') & ~Filters.command , get_name)],
        PHONE: [MessageHandler(Filters.regex('^(?!Cancel).*') & ~Filters.command, get_phone)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

# updater = Updater(TOKEN)

# # 加入 Handler
# updater.dispatcher.add_handler(conv_handler)




# # ===================================================================================================================

# if __name__ == "__main__":
#     # r = requests.get(Delete_WebhookInfo_URL)
#     # r = requests.get(Set_Webhook_URL)
#     # r = requests.get(Info_Webhook_URL)
#     # print(r.text)

#     app.run(host='0.0.0.0', port=5000, debug=True)