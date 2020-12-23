import csv
import json
from csv_converter import make_json
import sys

csv_file_path = 'data.csv'
json_file_path = 'data.json'


def try_to_create_file():
    try:
        open(json_file_path)
        return True
    except FileNotFoundError:
        try:
            make_json(csv_file_path, json_file_path)
            return False
        except FileNotFoundError:
            print('Ficheiro de dados (CSV) não encontrado.')
            return False


def print_menu():
    print('1. Jogar')
    print('2. Gerar o ficheiro a partir do CSV')
    print('3. Alterar dados de assistência')
    print('4. Eliminar dados de assistência')
    print('5. Consultar')
    print('6. Pesquisar')
    print('7. Total de espetadores')
    print('8. Informações de uma seleção')
    print('9. Eliminar ficheiro JSON')
    print('10. Sair\n')


def option_switch(option):
    if(option == 1):
        game()
    elif(option == 2):
        if(try_to_create_file()):
            print('O ficheiro já existe')
            return
    elif(option == 3):
        change_attendance_info()
    elif(option == 4):
        delete_attendance_info()
    elif(option == 5):
        try:
            opt = int(input('Deseja abrir o ficheiro JSON ou CSV? (1/2): '))

            if(opt == 1):
                print_json_file(json_file_path)
            elif(opt == 2):
                print_csv_file(csv_file_path)
            else:
                print('Deve inserir um número entre 1 e 2')
        except ValueError:
            print('Deve inserir um valor numérico')

    elif(option == 6):
        search_in_file()
    elif(option == 7):
        spectators = total_attendance()

        for info in spectators:
            print(
                str(info['year']) + ': ' + str(info['spectators']))
        print('\nNota: Nem todos os jogos têm informação atualizada quanto ao número de espetadores.')
    elif(option == 8):
        teams = get_all_teams(json_file_path)
        for team in teams:
            print(str(team['index']) + '. ' + team['team'])

        try:
            opt = int(input('Introduza uma opção: '))

            if (opt < 1 or opt > 81):
                print('Introduza uma opção válida.')
                return

            team_info = get_team_info(teams, opt)

            pretty_obj = pretiffy_json(team_info)

            print(pretty_obj)

        except ValueError:
            print('Deve introduzar um valor numérico')

    elif(option == 9):
        delete_json_file(json_file_path)
    elif(option == 10):
        sys.exit()
    else:
        print('Opção Inválida.')


def pretiffy_json(data):
    return json.dumps(data, indent=4)


def print_json_file(file_path):
    with open(file_path, 'r') as file:
        json_obj = json.load(file)

    pretty_obj = pretiffy_json(json_obj)

    print(pretty_obj)


def print_csv_file(file_path):
    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def get_all_teams(file_path):
    with open(file_path, 'r') as file:
        json_obj = json.load(file)

    teams = []

    for competition in json_obj:
        for game in competition['games']:
            if(not (game['home'] in teams)):
                teams.append(game['home'])

            if(not(game['away'] in teams)):
                teams.append(game['away'])

    teams.sort()

    data = []
    i = 1

    for team in teams:
        data.append({'index': i, 'team': team})
        i += 1

    return data


def total_attendance():
    with open(json_file_path, 'r') as file:
        json_obj = json.load(file)

    data = []

    for competition in json_obj:
        spectators = 0

        for game in competition['games']:
            if(game['attendance']):
                spectators += int(game['attendance'])

        data.append({'year': competition['year'], 'spectators': spectators})

    return data


def get_team_info(teams, index):
    team = teams[index - 1]['team']

    with open(json_file_path, 'r') as file:
        json_obj = json.load(file)

    team_data = []

    for competition in json_obj:
        for game in competition['games']:
            if(game['home'] == team or game['away'] == team):
                team_data.append(game)

    return team_data


def delete_json_file(path):
    import os

    try:
        os.remove(path)

        print('Ficheiro eliminado.')
    except OSError:
        print('Alguma coisa correu mal.')


def start():
    print_menu()

    try:
        option = int(input('Escolha uma opção: '))
        option_switch(option)
    except ValueError:
        print('Deve introduzir um valor numérico.')


start()
