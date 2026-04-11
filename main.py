import telebot
from config import TOKEN, DATABASE
from logic import DB_Manager
bot = telebot.TeleBot(TOKEN)
db = DB_Manager(DATABASE)
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, f"Привет, {message.from_user.first_name}! Я бот расписания уроков.")
    bot.send_message(message.chat.id, 'Введите свой класс')
    bot.register_next_step_handler(message, set_class)
def set_class(message): 
    cls = message.text
    result = db.add_user(message.from_user.id, cls)
    if result:
        bot.send_message(message.chat.id, 'Вы успешно зарегистрированы')
    else: 
        bot.send_message(message.chat.id, 'Вы уже зарегестрированы')
        

@bot.message_handler(commands=['help'])
def start(message):
    bot.reply_to(message, f"Привет, {message.from_user.first_name}! Список команд: /add - Добавляет урок")

@bot.message_handler(commands=['add'])
def add_lesson(message):




    bot.reply_to(message, "Урок добавлен!")


bot.infinity_polling()