from collections import namedtuple
from csv import DictReader

Location = namedtuple('Location', ['lng', 'lat', 'postal_code', 'city'])

test_locations = [
    Location("77.659309", "12.83957", "560100", 'Bangalore'),
    Location("80.1842321", "13.0205017", "600125", 'Chennai'),
    Location("77.251741", "28.551441", "110019", 'New Delhi')
]


def is_valid_reading(reading):
    required_fields = ['Latitude', 'Longitude', 'Postal Code', 'City']
    return all(reading[field] for field in required_fields)


def read(file_name):
    with open(file_name, 'r') as f:
        return [Location(r['Longitude'], r['Latitude'], r['Postal Code'], r['City']) for r in DictReader(f)
                if is_valid_reading(r)]
