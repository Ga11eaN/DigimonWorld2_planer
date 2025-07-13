import csv
import os


def read_enemies_data():
    with open('data/Enemies.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile, delimiter=';')
        return list(csv_reader)


def get_digi_names():
    digimon_names = []
    for f in os.listdir('data/images'):
        digimon_names.append(f.replace('.jpg', ''))
    return digimon_names
