import telebot
import sqlite3
from datetime import datetime, timedelta
import schedule
import time
import threading

API_TOKEN = '7992113857:AAEcKv8WFcBE_ld_-31gSUjkQpi_YOuxvFA'
bot = telebot.TeleBot(API_TOKEN)

# Используем SQLite для хранения данных о занятиях
conn = sqlite3.connect('schedule.db', check_same_thread=False)
c = conn.cursor()

# Создание таблицы для хранения расписания
c.execute('''
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    lesson_time TEXT,
    paid INTEGER DEFAULT 0
)
''')

# Функция для очистки базы данных (при необходимости)
def clear_database():
    c.execute("DELETE FROM lessons")  # Удаляет все записи из таблицы
    conn.commit()  # Сохраняем изменения
    print("База данных очищена.")

# Заполнение базы данных свободными слотами в рабочие дни
def initialize_schedule():
    c.execute("SELECT COUNT(*) FROM lessons")
    count = c.fetchone()[0]
    if count == 0:  # Если таблица пустая, заполняем слоты
        now = datetime.now()
        for i in range(7):  # Добавляем слоты на 7 дней вперед
            current_day = now + timedelta(days=i)
            if current_day.weekday() < 5:  # Рабочие дни (Пн-Пт)
                for hour in range(7, 15):  # Уроки с 7 до 14 (14 - последний слот)
                    lesson_time = current_day.strftime('%Y-%m-%d') + f" {hour}:00"
                    c.execute("SELECT COUNT(*) FROM lessons WHERE lesson_time = ?", (lesson_time,))
                    if c.fetchone()[0] == 0:  # Если слот не найден, вставляем его
                        c.execute("INSERT INTO lessons (lesson_time) VALUES (?)", (lesson_time,))
        conn.commit()
        print("Расписание инициализировано.")
    else:
        print("Расписание уже инициализировано, новые слоты не добавляются.")

initialize_schedule()

# Функция для отправки уведомлений
def send_notification(user_id, lesson_time):
    bot.send_message(message.chat.id, f"Напоминание: ваш урок начинается в {lesson_time}.")

# Асинхронный планировщик для отправки уведомлений
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск планировщика в отдельном потоке
threading.Thread(target=run_scheduler, daemon=True).start()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот для бронирования уроков\n"
                          "Используйте кнопки ниже:\n"
                          "/schedule - посмотреть расписание\n"
                          "/book + номер урока - забронировать урок\n"
                          "/occupied - мои уроки\n"
                          "/cancel + номер урока - отменить урок\n", reply_markup=create_keyboard())

# Функция для создания клавиатуры
def create_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row('/schedule', '/occupied')
    keyboard.row('/start', '/payment')
    return keyboard

# Обработчик команды /schedule
@bot.message_handler(func=lambda message: message.text == '/schedule')
def show_schedule(message):
    try:
        c.execute("SELECT * FROM lessons WHERE user_id IS NULL AND paid = 0")
        lessons = c.fetchall()
        if lessons:
            response = "Свободные слоты:\n"
            for lesson in lessons:
                date_time_obj = datetime.strptime(lesson[2], '%Y-%m-%d %H:%M')  # Соответствующий формат
                response += f"Урок {lesson[0]} в {date_time_obj.strftime('%H:%M')} {date_time_obj.strftime('%d.%m')}\n"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Нет свободных слотов.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при получении расписания: {str(e)}")

# Обработчик команды для бронирования урока
@bot.message_handler(func=lambda message: message.text.startswith('/book'))
def book_lesson(message):
    try:
        lesson_id = int(message.text.split()[1])  # Получаем ID урока из команды

        # Проверяем существование урока
        c.execute("SELECT * FROM lessons WHERE id = ?", (lesson_id,))
        lesson = c.fetchone()

        if lesson is None:
            bot.send_message(message.chat.id, "Ошибка: урок с таким ID не найден.")
            return

        # Проверяем, занято ли занятие
        c.execute("SELECT user_id FROM lessons WHERE id = ?", (lesson_id,))
        lesson_user = c.fetchone()

        if lesson_user[0] is not None:
            bot.send_message(message.chat.id, "Ошибка: урок уже забронирован.")
            return

        # Если все проверки пройдены, бронируем урок
        c.execute("UPDATE lessons SET user_id = ? WHERE id = ?", (message.from_user.id, lesson_id))
        conn.commit()

        lesson_time = lesson[2]
        notify_time = datetime.strptime(lesson_time, '%Y-%m-%d %H:%M')
        schedule_time = notify_time - timedelta(hours=1)
        schedule.every().day.at(schedule_time.strftime('%H:%M')).do(send_notification, message.from_user.id, lesson_time)

        bot.send_message(message.chat.id, f"Урок {lesson_id} забронирован на время {lesson_time}. Уведомление за час до занятия установлено.")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Пожалуйста, укажите корректный ID урока для бронирования.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при бронировании урока: {str(e)}")

# Обработчик команды для проверки занятых часов
@bot.message_handler(commands=['occupied'])
def show_occupied_hours(message):
    try:
        c.execute("SELECT * FROM lessons WHERE user_id = ? AND paid = 0", (message.from_user.id,))
        occupied = c.fetchall()
        if occupied:
            response = "Занятые слоты:\n"
            for lesson in occupied:
                date_time_obj = datetime.strptime(lesson[2], '%Y-%m-%d %H:%M')
                response += f"Урок {lesson[0]} в {date_time_obj.strftime('%H:%M')} {date_time_obj.strftime('%d.%m')}\n"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "У вас нет забронированных уроков.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при получении занятых часов: {str(e)}")

# Обработчик команды для отмены урока
@bot.message_handler(func=lambda message: message.text.startswith('/cancel'))
def cancel_lesson(message):
    try:
        lesson_id = int(message.text.split()[1])  # Получаем ID урока из команды
        c.execute("SELECT lesson_time FROM lessons WHERE id = ?", (lesson_id,))
        lesson = c.fetchone()

        if lesson is None:
            bot.send_message(message.chat.id, "Ошибка: урок с таким ID не найден.")
            return

        lesson_time = datetime.strptime(lesson[0], '%Y-%m-%d %H:%M')

        # Проверяем, остался ли час до начала занятия
        if datetime.now() >= lesson_time - timedelta(hours=1):
            bot.send_message(message.chat.id, "Отмена урока невозможна, так как осталось менее часа до начала.")
            return

        # Если все проверки пройдены, отменяем урок
        c.execute("UPDATE lessons SET user_id = NULL WHERE id = ?", (lesson_id,))
        conn.commit()
        bot.send_message(message.chat.id, f"Урок {lesson_id} отменен.")
    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Пожалуйста, укажите корректный ID урока для отмены.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при отмене урока: {str(e)}")

# Обработчик команды /payment
@bot.message_handler(commands=['payment'])
def payment_status(message):
    try:
        c.execute("SELECT COUNT(*) FROM lessons WHERE user_id = ? AND paid = 0", (message.from_user.id,))
        count = c.fetchone()[0]
        if count == 0:
            bot.send_message(message.chat.id, "Все занятия оплачены!")
        else:
            bot.send_message(message.chat.id, f"У вас осталось {count} неоплаченных занятия.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при проверке статуса оплаты: {str(e)}")

# Обработчик команды /pay
@bot.message_handler(commands=['pay'])
def pay_for_lessons(message):
    try:
        c.execute("UPDATE lessons SET paid = 1 WHERE user_id = ?", (message.from_user.id,))
        conn.commit()
        bot.reply_to(message, "Оплата завершена! Спасибо.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка при оплате: {str(e)}")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
