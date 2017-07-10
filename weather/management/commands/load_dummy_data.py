import csv
import os
from weather.models import WeatherModel
from datetime import date
from django.utils import timezone

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):        
        # WeatherModel.objects.all().delete()
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
                        except ValueError:
                            line[key] = 0
                db_lines.append(line)
                # print(line)
            # print([WeatherModel(**line) for line in db_lines])
            WeatherModel.objects.bulk_create([WeatherModel(**line) for line in db_lines])
                # print(instance.wind_direction)
