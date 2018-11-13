# FINAL

# Car Model { 'Brand': 'Honda', 'Model': 'Accord EX', 'Make': '2012' }

import csv
import unittest


class CarFinder:
    def __init__(self, *args, **kwargs):
        with open('cars.csv') as f:
            self.cars = list(csv.DictReader(f))

    def find_min_car(self):
        min_year = int(self.cars[0]['Make'])
        min_car = self.cars[0]

        for car in self.cars:
            if int(car['Make']) < min_year:
                min_year = int(car['Make'])
                min_car = car

        return min_car


class PrimesTestCase(unittest.TestCase):
    def test_car_finder(self):
        car_finder = CarFinder()
        min_car = car_finder.find_min_car()
        self.assertTrue(type(min_car['Brand']))
        self.assertTrue(type(min_car['Model']))
        self.assertTrue(min_car['Make'].isdigit())


def main():
    car_finder = CarFinder()
    min_car = car_finder.find_min_car()
    print(min_car['Brand'])
    print(min_car['Model'])
    print(min_car['Make'])


if __name__ == '__main__':
    # main()
    unittest.main()
