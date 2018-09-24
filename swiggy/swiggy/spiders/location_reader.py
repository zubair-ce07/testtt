from collections import namedtuple
from csv import DictReader

Location = namedtuple('Location', ['lng', 'lat', 'postal_code', 'city', 'locality'])

test_locations = [
    Location("77.659309", "12.83957", "560100", 'Bangalore', 'Electronic city phase -1, Next to hotel Svenska'),
    Location("80.1842321", "13.0205017", "600125", 'Chennai', 'Mount Poonamali high road,'),
    Location("77.251741", "28.551441", "110019", 'New Delhi', 'TDI mall, Nehru place metro station, Nehru place')
]


def is_valid_reading(reading):
    required_fields = ['Latitude', 'Longitude', 'Postal Code', 'City', 'Address Line 2']
    return all(reading[field] for field in required_fields)


def read(file_name):
    with open(file_name, 'r') as f:
        return [Location(r['Longitude'], r['Latitude'], r['Postal Code'], r['City'], r['Address Line 2'])
                for r in DictReader(f) if is_valid_reading(r)]
