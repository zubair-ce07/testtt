import csv
from wundergroundspider import settings
import os


class WeatherItemPipeline(object):
    def process_item(self, item, spider):
        file_name = "{}_weather_{}_{}.csv".format(item['city'], item['year'], item['month'])
        file_full_name = os.path.join(os.path.basename(settings.csv_file_path), file_name)
        writer = csv.writer(open(file_full_name, 'w'), delimiter='\n', lineterminator='\n')
        writer.writerow([row.strip() for row in item['weather_rows']])
        return item
