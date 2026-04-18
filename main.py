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
        bot.send_message(message.chat.id, 'Вы уже зарегистрированы')  # ИСПРАВЛЕНО: опечатка "зарегестрированы"

@bot.message_handler(commands=['help'])
def help_command(message):  # ИСПРАВЛЕНО: имя функции с start на help_command
    bot.reply_to(message, f"{message.from_user.first_name}! Список команд: \n/add - Добавить урок\n/get - Получить расписание")

@bot.message_handler(commands=['add'])
def add_lesson(message):
    # Создаем таблицы, если их нет (добавлено для безопасности)
    db.create_tables()
    bot.reply_to(message, f"{message.from_user.first_name}, давай добавим урок!")
    bot.send_message(message.chat.id, 'Введите: день недели, номер урока, название предмета, время начала, время окончания, класс\nПример: пн 1 Математика 08:30 09:10 5А')
    bot.register_next_step_handler(message, set_lesson)

def set_lesson(message):
    try:
        data = message.text.split()
        if len(data) != 6:
            bot.send_message(message.chat.id, 'Ошибка! Введите 6 параметров через пробел\nПример: пн 1 Математика 08:30 09:10 5А')
            bot.register_next_step_handler(message, set_lesson)
            return
        
        weekend, number_lessen, name_lessen, time_start, time_end, class_name = data
        # Преобразуем номер урока в число
        number_lessen = int(number_lessen)
        
        result = db.add_lessen(weekend, number_lessen, name_lessen, time_start, time_end, class_name)
        
        if result:
            bot.send_message(message.chat.id, f'Урок {name_lessen} для {class_name} класса успешно добавлен')
        else:
            bot.send_message(message.chat.id, 'Ошибка при добавлении урока')
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка! Номер урока должен быть числом\nПример: пн 1 Математика 08:30 09:10 5А')
        bot.register_next_step_handler(message, set_lesson)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')

@bot.message_handler(commands=['get'])
def get_rasp(message):
    try:
        # Получаем класс пользователя
        user_class = db.get_class(message.from_user.id)
        if user_class is None:
            bot.send_message(message.chat.id, 'Вы не зарегистрированы! Используйте команду /start')
            return
        
        # Получаем расписание для класса
        result = db.return_lessens(user_class)  # ИСПРАВЛЕНО: return_lessens вместо get_lessens
        
        if not result:
            bot.send_message(message.chat.id, f'Расписание для {user_class} класса не найдено')
            return
        
        # Форматируем вывод расписания
        rasp_text = f"📚 РАСПИСАНИЕ ДЛЯ {user_class} КЛАССА 📚\n\n"
        for row in result:
            # row: (id, weekend, number_lessen, name_lessen, time_start, time_end, class)
            rasp_text += f"📌 {row[1].upper()} | Урок {row[2]}\n"
            rasp_text += f"📖 {row[3]}\n"
            rasp_text += f"⏰ {row[4]} - {row[5]}\n"
            rasp_text += f"🏫 {row[6]} класс\n"
            rasp_text += "-" * 30 + "\n"
        
        bot.send_message(message.chat.id, rasp_text)
        
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка при получении расписания: {e}')

# Добавляем команду для просмотра всех уроков (для отладки)
@bot.message_handler(commands=['all'])
def get_all(message):
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Lessens")
        rows = cursor.fetchall()
        conn.close()
        
        if rows:
            text = "ВСЕ УРОКИ В БАЗЕ:\n\n"
            for row in rows:
                text += f"{row}\n"
            bot.send_message(message.chat.id, text)
        else:
            bot.send_message(message.chat.id, "База пуста")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

if __name__ == '__main__':
    # Создаем таблицы при запуске
    db.create_tables()
    print("Бот запущен...")
    bot.infinity_polling()