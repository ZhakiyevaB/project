import telebot
from telebot import types

BOT_TOKEN = '6650684706:AAHRDIYIAp4tQJWr9N84FyfYMAub_p_o6fA'
bot = telebot.TeleBot(BOT_TOKEN)
questions = [
    {"question": "Какой цвет волос у твоего персонажа?", "options": ["Желтый", "Розовый", "Черный", "Серый"]},
    {"question": "Какая техника твоего персонажа в Наруто?", "options": ["Рассенган", "Кулак", "Огненный шар", "Копье тени"]},
    {"question": "Какой характер твоего персонажа?", "options": ["Эксцентричный", "Боевой", "Задумчивый", "Спокойный"]}
]

characters = {
    "Наруто": {"hair_color": "Желтый", "technique": "Рассенган", "character": "Эксцентричный"},
    "Сакура": {"hair_color": "Розовый", "technique": "Кулак", "character": "Боевой"},
    "Саске": {"hair_color": "Черный", "technique": "Огненный шар", "character": "Задумчивый"},
    "Какаши": {"hair_color": "Серый", "technique": "Копье тени", "character": "Спокойный"}
}

user_answers = {}
@bot.message_handler(commands=['info'])
def info(message):
    bot.send_message(message.chat.id, 'Я бот для игр, нажми /start чтобы начать игру!')

@bot.message_handler(commands=['start','quiz'])
def handle_start(message):
    user_id = message.from_user.id
    user_answers[user_id] = {"answers": [], "current_question": 0}
    ask_question(user_id)

@bot.message_handler(func=lambda message: True)
def handle_answer(message):
    user_id = message.from_user.id
    current_question = user_answers[user_id]["current_question"]

    if current_question < len(questions):
        user_response = message.text
        user_answers[user_id]["answers"].append(user_response)
        user_answers[user_id]["current_question"] += 1
        ask_question(user_id)
    else:
        finish_quiz(user_id)

def ask_question(user_id):
    current_question = user_answers[user_id]["current_question"]

    if current_question < len(questions):
        question_data = questions[current_question]
        question_text = question_data["question"]
        options = question_data["options"]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for option in options:
            markup.add(types.KeyboardButton(option))

        bot.send_message(user_id, f"{question_text}", reply_markup=markup)
    else:
        finish_quiz(user_id)

def finish_quiz(user_id):
    user_responses = user_answers[user_id]["answers"]
    character = determine_character(user_responses)
    bot.send_message(user_id, f"Тест завершен! Ваш персонаж: {character}\n")


def determine_character(user_responses):
    for char, char_data in characters.items():
        if all(response in char_data.values() for response in user_responses):
            return char
    return "Какаши"

bot.polling()
