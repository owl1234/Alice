def handler(event, context):
    import random
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """

    if event['session']['new']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "1", "riddle": "-1"},
            'response': {
                'text': 'Привет! Давай поиграем в быки и коровы. Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и угадано с полным совпадением (быки). Называть числа нужно строго без повторяющихся цифр. Какое число загадать?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Хорошо", "Повтори правила", "Не хочу играть"]],
                'end_session': 'false'
            },
        }

    if event['request']['original_utterance'].lower() == 'хорошо':
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": event['state']['session']['status'], "riddle": event['state']['session']['riddle']},
            'response': {
                'text': 'Какое число загадать?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Однозначное", "Двузначное", "Трёхзначное", "Четырёхзначное"]],
                'end_session': 'false'
            },
        }

    if 'правила' in event['request']['original_utterance'].lower():
        if event['state']['session']['status'] == "1": # если число ещё не загадано
            return {
                'version': event['version'],
                'session': event['session'],
                'session_state': {"status": event['state']['session']['status'],
                                  "riddle": event['state']['session']['riddle']},
                'response': {
                    'text': 'Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и угадано с полным совпадением (быки). Называть числа нужно строго без повторяющихся цифр. Какое число загадать?',
                    'buttons': [{'title': suggest, 'hide': True} for suggest in ["Однозначное", "Двузначное", "Трёхзначное", "Четырёхзначное", "Повтори правила", "Не хочу играть"]],
                    'end_session': 'false'
                },
            }
        elif event['state']['session']['status'] == "2": # повтор правил
            return {
                'version': event['version'],
                'session': event['session'],
                'session_state': {"status": event['state']['session']['status'],
                                  "riddle": event['state']['session']['riddle']},
                'response': {
                    'text': 'Я загадываю число, а Вы пытаетесь его отгадать. После Вашей попытки я говорю, сколько цифр угадано без совпадения с их позициями в моём числе (коровы) и угадано с полным совпадением (быки). Как вы думаете, какое число я загадала? %s' % (event),
                    'buttons': [{'title': suggest, 'hide': True} for suggest in ["Подсказка", "Сдаюсь"]],
                    'end_session': 'false'
                },
            }

    if event['request']['original_utterance'].lower() in ['не хочу играть', 'нет']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": event['state']['session']['status'],
                              "riddle": event['state']['session']['riddle']},
            'response': {
                'text': 'Поняла',
                'end_session': 'true'
            },
        }

    if event['request']['original_utterance'].lower() == 'однозначное':
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "2",
                              "riddle": str(random.randint(0, 9))},
            'response': {
                'text': 'Хорошо, я загадала. Как вы думаете, какое это число?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
                'end_session': 'false'
            },
        }

    if event['request']['original_utterance'].lower() == 'двузначное':
        now = random.randint(10, 99)
        while len(set(str(now))) != 2:
            now = random.randint(10, 99)
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "2",
                              "riddle": str(now)},
            'response': {
                'text': 'Хорошо, я загадала. Как вы думаете, какое это число?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
                'end_session': 'false'
            },
        }

    if event['request']['original_utterance'].lower() == 'трёхзначное':
        now = random.randint(100, 999)
        while len(set(str(now))) != 3:
            now = random.randint(100, 999)
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "2",
                              "riddle": str(now)},
            'response': {
                'text': 'Хорошо, я загадала. Как вы думаете, какое это число?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
                'end_session': 'false'
            },
        }

    if event['request']['original_utterance'].lower() == 'четырёхзначное':
        now = random.randint(1000, 9999)
        while len(set(str(now))) != 4:
            now = random.randint(1000, 9999)
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "2",
                              "riddle": str(now)},
            'response': {
                'text': 'Хорошо, я загадала. Как вы думаете, какое это число?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
                'end_session': 'false'
            },
        }

    if event['request']['original_utterance'].lower() in ['сдаюсь', 'хватит']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "3",
                              "riddle": event['state']['session']['riddle']},
            'response': {
                'text': 'На самом деле, всё очень просто. Я загадала число %s. Хотите сыграть ещё раз?' % str(event['state']['session']['riddle']),
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Да", "Нет"]],
                'end_session': 'false'
            },
        }

    if event['request']['original_utterance'].lower() == 'да' and event['state']['session']['status'] == "3":
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "1",
                              "riddle": "-1"},
            'response': {
                'text': 'Какое число загадать?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in
                            ["Однозначное", "Двузначное", "Трёхзначное", "Четырёхзначное", "Повтори правила",
                             "Не хочу играть"]],
                            'end_session': 'false'
            },
        }

    if event['request']['original_utterance'].lower() == 'подсказка':
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": event['state']['session']['status'],
                              "riddle": event['state']['session']['riddle']},
            'response': {
                'text': 'В этом числе есть цифра %s.' % (random.choice([i for i in event['state']['session']['riddle']])),
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
                            'end_session': 'false'
            },
        }

    for i in event['request']['original_utterance']:
        if i not in "0123456789":
            return {
                'version': event['version'],
                'session': event['session'],
                'session_state': {"status": event['state']['session']['status'],
                                  "riddle": event['state']['session']['riddle']},
                'response': {
                    'text': 'Кажется, вы ввели что-то не то. Введите число ещё раз.',
                    'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
                    'end_session': 'false'
                },
            }


    if len(event['request']['original_utterance']) != len(event['state']['session']['riddle']):
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": event['state']['session']['status'],
                              "riddle": event['state']['session']['riddle']},
            'response': {
                'text': 'Количество цифр в вашем числе не совпадает с количеством цифр в загаданном числе. Назовите число ещё раз.',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
                'end_session': 'false'
            },
        }

    if str(event['request']['original_utterance']) == event['state']['session']['riddle']:
        return {
            'version': event['version'],
            'session': event['session'],
            'session_state': {"status": "3",
                              "riddle": event['state']['session']['riddle']},
            'response': {
                'text': 'Ура-ура, число угадано, вы большой молодец! Хорошая игра. Хотите сыграть ещё раз?',
                'buttons': [{'title': suggest, 'hide': True} for suggest in ["Да", "Нет"]],
                'end_session': 'false'
            },
        }

    bulls = cows = 0
    for i in range(len(event['state']['session']['riddle'])):
        if event['state']['session']['riddle'][i] == str(event['request']['original_utterance'])[i]:
            bulls += 1

    for i in str(event['request']['original_utterance']):
        for j in event['state']['session']['riddle']:
            if i == j:
                cows += 1

    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {"status": event['state']['session']['status'],
                          "riddle": event['state']['session']['riddle']},
        'response': {
            'text': 'Коров: %s, быков: %s' % (cows - bulls, bulls),
            'buttons': [{'title': suggest, 'hide': True} for suggest in ["Сдаюсь", "Подсказка"]],
            'end_session': 'false'
        },
    }








    return {
        'version': event['version'],
        'session': event['session'],
        'session_state': {"status": event['state']['session']['status'], "riddle": event['state']['session']['riddle']},
        'response': {
            'text': 'Странные вы все какие-то... %s' % (event),
            'end_session': 'false'
        },
    }