from csv_converter import make_json

def start():
    try:
        data_file = open('data.json')
    except FileNotFoundError:
        try:
            make_json('data.csv', 'data.json')
        except FileNotFoundError:
            print('No data file found.')



start()
