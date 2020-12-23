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
        total_attendance()
    elif(option == 8):
        team_info()
    elif(option == 9):
        delete_json_file()
    elif(option == 10):
        sys.exit()
    else:
        print('Opção Inválida.')


def print_json_file(file_path):
    with open(file_path, 'r') as file:
        json_obj = json.load(file)

    pretty_obj = json.dumps(json_obj, indent=4)

    print(pretty_obj)


def print_csv_file(file_path):
    data = {}

    with open(file_path, newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)


def start():
    print_menu()

    try:
        option = int(input('Escolha uma opção: '))
        option_switch(option)
    except ValueError:
        print('Deve introduzir um valor numérico.')


start()
