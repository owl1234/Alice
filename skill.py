# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
import random

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

status = 0
riddle = -1
def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        sessionStorage[user_id] = {
            'suggests': [
                "Хорошо",
                "Повтори правила",
                "Не хочу играть",
            ]
        }
        res['response']['text'] = 'Привет! Давай поиграем в быки и коровы. Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и не угадано (быки). Какое число загадать?'
        res['response']['buttons'] = get_suggests(user_id)
        status = 1
        return

    if req['request']['original_utterance'].lower() == 'хорошо':
        res['response']['text'] = 'Какое число загадать?'
        sessionStorage[user_id] = {
            'suggests': [
                "Однозначное",
                "Двузначное",
                "Трёхзначное",
                "Четырёхзначное"
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    if 'правила' in req['request']['original_utterance'].lower():
        if status == 1: # если число ещё не загадано
            res['response']['text'] = 'Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и угадано с полным совпадением (быки). Какое число загадать?'
            sessionStorage[user_id] = {
                'suggests': [
                    "Однозначное",
                    "Двузначное",
                    "Трёхзначное",
                    "Четырёхзначное"
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
        else if status == 2: # повтор правил
            res['response']['text'] = 'Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и угадано с полным совпадением (быки). Как вы думаете, какое число я загадала?'
        return

    if req['request']['original_utterance'].lower() in ['не хочу', 'нет']:
        res['response']['text'] = 'Поняла.'
        return

    if req['request']['original_utterance'].lower() == 'однозначное':
        status = 2
        riddle = random.randint(0, 9)
        res['response']['text'] = 'Хорошо, я загадала. Как вы думаете, какое это число?'
        sessionStorage[user_id] = {
            'suggests': [
                "Сдаюсь",
                "Подсказка",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() == 'двузначное':
        status = 2
        riddle = random.randint(10, 99)
        res['response']['text'] = 'Хорошо, я загадала. Как вы думаете, какое это число?'
        sessionStorage[user_id] = {
            'suggests': [
                "Сдаюсь",
                "Подсказка",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() == 'трёхзначное':
        status = 2
        riddle = random.randint(100, 999)
        res['response']['text'] = 'Хорошо, я загадала. Как вы думаете, какое это число?'
        sessionStorage[user_id] = {
            'suggests': [
                "Сдаюсь",
                "Подсказка",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() == 'четырёхзначное':
        status = 2
        riddle = random.randint(1000, 9999)
        res['response']['text'] = 'Хорошо, я загадала. Как вы думаете, какое это число?'
        sessionStorage[user_id] = {
            'suggests': [
                "Сдаюсь",
                "Подсказка",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() == 'сдаюсь':
        status = 3
        res['response']['text'] = 'На самом деле, всё очень просто. Я загадала число %s. Хотите сыграть ещё раз?' % str(riddle)
        sessionStorage[user_id] = {
            'suggests': [
                "Да",
                "Нет",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() == 'Да' and status == 3:
        status = 1
        res['response']['text'] = 'Какое число загадать?'
        sessionStorage[user_id] = {
            'suggests': [
                "Однозначное",
                "Двузначное",
                "Трёхзначное",
                "Четырёхзначное"
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    if req['request']['original_utterance'].lower() == 'подсказка':
        res['response']['text'] = 'В этом числе есть цифра %s.' % (random.choice([i for i in str()]))
        sessionStorage[user_id] = {
            'suggests': [
                "Сдаюсь",
                "Подсказка",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    for i in type(req['request']['original_utterance']):
        if i not in '0123456789':
            res['response']['text'] = 'Кажется, вы ввели что-то не то. Давайте попробуем ещё раз?'
            res['response']['buttons'] = get_suggests(user_id)
            return

    if len(req['request']['original_utterance']) != len(str(riddle)):
        res['response']['text'] = 'Количество цифр в вашем числе не совпадает с количеством цифр в загаданном числе. Назовите число ещё раз.'
        res['response']['buttons'] = get_suggests(user_id)
        return

    str_riddle = str(riddle)
    if req['request']['original_utterance'] == str_riddle:
        status = 3 # конец игры
        res['response']['text'] = 'Ура-ура, число угадано, вы большой молодец! Хорошая игра. Хотите сыграть ещё раз?'
        sessionStorage[user_id] = {
            'suggests': [
                "Да",
                "Нет",
            ]
        }
        res['response']['buttons'] = get_suggests(user_id)
        return

    bulls = cows = 0
    for i in range(len(str_riddle)):
        if str_riddle[i] == req['request']['original_utterance'][i]:
            bulls += 1

    for i in req['request']['original_utterance']:
        for j in str_riddle:
            if i == j:
                cows += 1
    res['response']['text'] = 'Коров: "%s", быков: %s' % (cows - bulls, bulls)
    res['response']['buttons'] = get_suggests(user_id)
    sessionStorage[user_id] = {
        'suggests': [
            "Сдаюсь",
            "Подсказка",
        ]
    }

# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    # session['suggests'] = session['suggests'][1:]
    # sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    # if len(suggests) < 2:
    #     suggests.append({
    #         "title": "Ладно",
    #         "url": "https://market.yandex.ru/search?text=слон",
    #         "hide": True
    #    })

    return suggests