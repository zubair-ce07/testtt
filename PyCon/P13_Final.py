# FINAL

import csv


def find_min_car(cars):
    min_year = int(cars[0]['Make'])
    min_car = cars[0]

    for car in cars:
        if int(car['Make']) < min_year:
            min_year = int(car['Make'])
            min_car = car

    return min_car


def main():
    with open('cars.csv') as f:
        cars = list(csv.DictReader(f))

    min_car = find_min_car(cars)
    print(min_car['Brand'])
    print(min_car['Model'])
    print(min_car['Make'])


if __name__ == '__main__':
    main()
