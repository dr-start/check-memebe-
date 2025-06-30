import telebot
from flask import Flask, request

TOKEN = '7571450526:AAG851D0us9kOdlWkTF8OcEiY2Er-pS4qpY'
CHANNEL_ID = '@SafeNet_V2ray'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn = telebot.types.InlineKeyboardButton("✅ عضو شدم", callback_data="check")
    markup.add(btn)
    bot.send_message(message.chat.id, f"سلام! لطفاً ابتدا عضو {CHANNEL_ID} شو و سپس روی دکمه زیر بزن.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check(call):
    status = bot.get_chat_member(CHANNEL_ID, call.from_user.id).status
    if status in ['member', 'administrator', 'creator']:
        bot.send_message(call.message.chat.id, "✅ عضو شدی! اینم لینک:
https://example.com/your-link")
    else:
        bot.send_message(call.message.chat.id, "❌ هنوز عضو نیستی!")

@app.route('/')
def index():
    return "Bot is alive!"

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://YOUR-RENDER-URL.onrender.com/' + TOKEN)
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
