import json
from random import randint

n_of_options_per_question = 4
max_bias = 1


def play(json_file_path):
    clear_console()
    try:
        with open(json_file_path, 'r') as file:
            json_obj = json.load(file)

        competition = generate_random_object(json_obj)
        game = generate_random_object(competition['games'])

        options = generate_options(game)

        question_str = elaborate_question(competition, game, options)

        print(question_str)

        try:
            answer = input('\nSelecione a opção correta: ')
        except ValueError:
            print('Selecione uma opção de valor numérico')

    except FileNotFoundError:
        print('Ocorreu um erro na leitura do ficheiro JSON')
        print('Verifique se o ficheiro já foi criado.')


def generate_random_object(data):
    random_index = randint(0, len(data) - 1)

    return data[random_index]


def generate_options(game):
    home_score = int(game['h_score'])
    away_score = int(game['a_score'])

    options = []

    correct = f'{home_score}-{away_score}'

    options.append(correct)

    i = 1

    while i < n_of_options_per_question:
        new_option = generate_wrong_option(home_score, away_score)

        if(new_option in options):
            continue
        else:
            options.append(new_option)
            i += 1

    import random

    random.shuffle(options)

    return options


def generate_wrong_option(home_score, away_score):
    bias = randint(0, 1)

    if(bias == 1):  # Sum
        wrong_home_score = home_score + randint(1, max_bias)
    else:  # Subtract
        wrong_home_score = home_score - randint(1, max_bias)
        if(wrong_home_score < 0):
            wrong_home_score = 0

    bias = randint(0, 1)

    if(bias == 1):  # Sum
        wrong_away_score = away_score + randint(1, max_bias)
    else:  # Subtract
        wrong_away_score = away_score - randint(1, max_bias)

        if(wrong_away_score < 0):
            wrong_away_score = 0

    if(wrong_home_score == home_score and wrong_away_score == away_score):
        generate_wrong_option(home_score, away_score)

    return f'{wrong_home_score}-{wrong_away_score}'


def elaborate_question(competition, game, options):
    year = competition['year']
    host = competition['host']
    home_team = game['home']
    away_team = game['away']

    options_str = ''

    i = 0

    for option in options:
        options_str += f'{i+1}. {option}    '
        i += 1

    return f'Ano: {year}\nLocal: {host}\nJogo entre: {home_team} x {away_team}\n\n Resultado:\n\n {options_str}'


def clear_console():
    import os

    os.system('cls' if os.name == 'nt' else 'clear')
