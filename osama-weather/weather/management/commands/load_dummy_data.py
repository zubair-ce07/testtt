import csv
import os
from datetime import date

from django.utils import timezone
from django.core.management.base import BaseCommand

from weather.models import WeatherModel


class LoadDummyData(BaseCommand):
    '''
    command to load data in DATA_FILE to the db
    '''

    def handle(self, **options):
        os.system('./manage.py flush --noinput')
        with open('madrid.csv', 'r') as csvfile:
            lines = csv.DictReader(csvfile)
            db_lines = []
            for line in lines:
                line.pop('max_wind_speed')
                line.pop('mean_wind_speed')
                line.pop('max_gust_speed')
                line.pop('precipitation')
                line.pop('cloud_cover')
                line.pop('events')
                line.pop('wind_direction')
                for key in line:
                    if key != 'date':
                        try:
                            line[key] = float(line[key])
                        except:
                            pass
                db_lines.append(line)
            WeatherModel.objects.bulk_create(
                [WeatherModel(**line) for line in db_lines])
