# @medsech21bot
import telebot
from telebot import types
import psycopg2
import joblib
import numpy as np
from llm_part import ask_gigachat, connect_gigachat

model1 = joblib.load("model.pkl")

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="mysecretpassword",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()

bot = telebot.TeleBot('7560682323:AAH1t1oZiktAS8NNRAeRdgvOJFQC_AIYKA8')
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    ask_gender(message.chat.id)


def ask_gender(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Мужчина", callback_data='gender_1'),
        types.InlineKeyboardButton("Женщина", callback_data='gender_0')
    )
    bot.send_message(chat_id, "Выберите ваш пол:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('gender'))
def process_gender(call):
    user_id = call.from_user.id
    user_data[user_id]['gender'] = int(call.data.split('_')[1])
    ask_age(call.message.chat.id)


def ask_age(chat_id):
    msg = bot.send_message(chat_id, "Введите ваш возраст:")
    bot.register_next_step_handler(msg, process_age_step)


def process_age_step(message):
    try:
        user_id = message.from_user.id
        age = int(message.text)
        if age < 0 or age > 120:
            raise ValueError()
        user_data[user_id]['age'] = age
        ask_hypertension(message.chat.id)
    except:
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите корректный возраст (0-120):")
        bot.register_next_step_handler(msg, process_age_step)


def ask_hypertension(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Да", callback_data='hypertension_1'),
        types.InlineKeyboardButton("Нет", callback_data='hypertension_0')
    )
    bot.send_message(chat_id, "Есть ли у вас гипертония?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('hypertension'))
def process_hypertension(call):
    user_id = call.from_user.id
    user_data[user_id]['hypertension'] = int(call.data.split('_')[1])
    ask_heart_disease(call.message.chat.id)


def ask_heart_disease(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Да", callback_data='heart_1'),
        types.InlineKeyboardButton("Нет", callback_data='heart_0')
    )
    bot.send_message(chat_id, "Есть ли у вас заболевания сердца?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('heart'))
def process_heart_disease(call):
    user_id = call.from_user.id
    user_data[user_id]['heart_disease'] = int(call.data.split('_')[1])
    ask_marital_status(call.message.chat.id)


def ask_marital_status(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Да", callback_data='married_1'),
        types.InlineKeyboardButton("Нет", callback_data='married_0')
    )
    bot.send_message(chat_id, "Вы когда-либо состояли в браке?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('married'))
def process_marital_status(call):
    user_id = call.from_user.id
    user_data[user_id]['ever_married'] = int(call.data.split('_')[1])
    ask_work_type(call.message.chat.id)


def ask_work_type(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Я ребенок", callback_data='work_0'),
        types.InlineKeyboardButton("Госслужащий", callback_data='work_1'),
        types.InlineKeyboardButton("Никогда не работал", callback_data='work_2'),
        types.InlineKeyboardButton("Негосударственная работа", callback_data='work_3'),
        types.InlineKeyboardButton("Самозанятый", callback_data='work_4')
    )
    bot.send_message(chat_id, "Выберите ваш тип занятости:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('work'))
def process_work_type(call):
    user_id = call.from_user.id
    user_data[user_id]['work_type'] = int(call.data.split('_')[1])
    ask_residence_type(call.message.chat.id)


def ask_residence_type(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Город", callback_data='residence_1'),
        types.InlineKeyboardButton("Село", callback_data='residence_0')
    )
    bot.send_message(chat_id, "Выберите тип вашего проживания:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('residence'))
def process_residence_type(call):
    user_id = call.from_user.id
    user_data[user_id]['residence_type'] = int(call.data.split('_')[1])
    ask_glucose(call.message.chat.id)


def ask_glucose(chat_id):
    msg = bot.send_message(chat_id, "Введите средний уровень глюкозы в крови (ммоль/л):")
    bot.register_next_step_handler(msg, process_glucose_step)


def process_glucose_step(message):
    try:
        user_id = message.from_user.id
        glucose = float(message.text.replace(',', '.'))
        if glucose < 2 or glucose > 30:
            raise ValueError()
        user_data[user_id]['avg_glucose_level'] = glucose
        ask_bmi(message.chat.id)
    except:
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите значение между 2 и 30 (например: 5.4):")
        bot.register_next_step_handler(msg, process_glucose_step)


def ask_bmi(chat_id):
    msg = bot.send_message(chat_id, "Введите ваш ИМТ:")
    bot.register_next_step_handler(msg, process_bmi_step)


def process_bmi_step(message):
    try:
        user_id = message.from_user.id
        bmi = float(message.text.replace(',', '.'))
        if bmi < 10 or bmi > 50:
            raise ValueError()
        user_data[user_id]['bmi'] = bmi
        ask_smoking_status(message.chat.id)
    except:
        msg = bot.send_message(message.chat.id, "Пожалуйста, введите значение между 10 и 50 (например: 22.5):")
        bot.register_next_step_handler(msg, process_bmi_step)


def ask_smoking_status(chat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Ранее курил(а)", callback_data='smoking_0'),
        types.InlineKeyboardButton("Никогда не курил(а)", callback_data='smoking_1'),
        types.InlineKeyboardButton("Курю", callback_data='smoking_2'),
        types.InlineKeyboardButton("Неизвестно", callback_data='smoking_3')
    )
    bot.send_message(chat_id, "Выберите ваш статус курения:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith('smoking'))
def process_smoking_status(call):
    user_id = call.from_user.id
    user_data[user_id]['smoking_status'] = int(call.data.split('_')[1])
    make_prediction(call.message.chat.id, user_id)


def make_prediction(chat_id, user_id):
    try:
        user = user_data[user_id]
        input_data = [[
            user['gender'],
            user['age'],
            user['hypertension'],
            user['heart_disease'],
            user['ever_married'],
            user['work_type'],
            user['residence_type'],
            user['avg_glucose_level'],
            user['bmi'],
            user['smoking_status']
        ]]

        prediction = float(model1.predict_proba(np.array(input_data))[0][1])
        risk_category = get_risk_category(prediction)

        cursor.execute("""
            INSERT INTO predictions (
                gender, age, hypertension, heart_disease, 
                ever_married, work_type, residence_type, 
                avg_glucose_level, bmi, smoking_status, 
                prediction
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            user['gender'],
            user['age'],
            user['hypertension'],
            user['heart_disease'],
            user['ever_married'],
            user['work_type'],
            user['residence_type'],
            user['avg_glucose_level'],
            user['bmi'],
            user['smoking_status'],
            prediction
        ))
        conn.commit()

        result = f"""Результаты анализа:

Вероятность инсульта: {prediction * 100:.1f}%
Категория риска: {risk_category}"""

        bot.send_message(chat_id, result)
        recomendation(chat_id, user_id)

    except Exception as e:
        bot.send_message(chat_id, "Произошла ошибка при обработке данных. Пожалуйста, попробуйте снова.")
        print(f"Error: {str(e)}")


def get_risk_category(prediction):
    if prediction < 0.2:
        return "Крайне низкий"
    elif prediction < 0.4:
        return "Низкий"
    elif prediction < 0.6:
        return "Умеренный"
    elif prediction < 0.8:
        return "Высокий"
    else:
        return "Крайне высокий"


def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Новый анализ'))
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Новый анализ')
def new_analysis(message):
    start(message)

def recomendation(chat_id, user_id):
    try:
        user = user_data[user_id]
        model = connect_gigachat()
        prompt = f'''Я хочу получить персонализированные рекомендации по снижению риска инсульта на основе предоставленных мною данных. Твоя задача - проанализировать информацию, которую я предоставлю, и выдать подробные, практически применимые советы, учитывающие все мои индивидуальные особенности. Рекомендации должны охватывать следующие области:

        •  Диета: Конкретные примеры продуктов, которые стоит добавить или исключить из рациона, с учетом возможных ограничений и личных предпочтений.
        •  Физическая активность: Рекомендации по подходящим видам активности, их интенсивности, частоте и продолжительности, с учетом моего типа работы и физического состояния.
        •  Управление стрессом: Практики и техники для снижения уровня стресса, адаптированные к моему образу жизни и возможностям.
        •  Медикаментозное лечение (если необходимо): Упоминание о необходимости консультации с врачом для обсуждения возможности применения медикаментов, если мои данные указывают на повышенный риск и это необходимо.
        •  Изменение образа жизни: Конкретные шаги, которые я могу предпринять для улучшения своего здоровья в целом и снижения риска инсульта.
        •  Дополнительные рекомендации: Любые другие советы, которые могут быть полезны, учитывая мою индивидуальную ситуацию.

        Формат ответа:
        Длина одного сообщения: до 500 символов.
        Пожалуйста, предоставь небольшие рекомендации в структурированном формате, разбив их по вышеуказанным категориям (Диета, Физическая активность, Управление стрессом, Медикаментозное лечение, Изменение образа жизни, Дополнительные рекомендации). Каждая рекомендация должна быть конкретной и понятной, с объяснением ее важности для снижения риска инсульта.

        Параметры пользователя (замените значения на реальные данные):

        •  Пол: {user['gender']}
        •  Возраст: {user['age']}
        •  Наличие гипертонии: {user['hypertension']}
        •  Наличие болезней сердца: {user['heart_disease']}
        •  Тип работы: {user['work_type']}
        •  Место проживания: {user['residence_type']}
        •  Средний уровень глюкозы в крови (натощак): {user['avg_glucose_level']}
        •  Индекс массы тела (ИМТ): {user['bmi']}
        •  Статус курения: {user['smoking_status']}

        •  Учитывайте последние рекомендации медицинских организаций (например, AHA/ASA) по профилактике инсульта.
        •  Не предоставляйте медицинские советы, заменяющие консультацию врача. Подчеркните необходимость консультации с квалифицированным медицинским специалистом.
        •  Укажите, какие факторы риска инсульта я имею, исходя из предоставленных данных.
        '''

        result = ask_gigachat(model, prompt)

        bot.send_message(chat_id, result)
        send_main_menu(chat_id)

    except Exception as e:
        bot.send_message(chat_id, "Не получилось подобрать для Вас персональные рекомендации. Рекомендуем связаться с врачом!")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    bot.polling()
