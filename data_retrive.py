import csv


def read_enemies_data():
    with open('data/Enemies.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')
        return list(csv_reader)
