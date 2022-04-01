import telebot
import os
from flask import Flask, request
import logging

token = '5178608519:AAGqDLaQzbTEuyaGC5R9-LoZ45Y_8DxQ3Qg'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types='text')
def start_message(message):
    # if message.text == 'ok':
    try:
        bot.send_message(message.chat.id, message.text)
    except Exception as _ex:
        bot.send_message(message.chat.id, _ex)


# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200
    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://erstwebhookandv.herokuapp.com/") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)