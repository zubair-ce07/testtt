Weatherman Django
=======

This is a Django App of Weatherman

## Custom command

To Load weather data from files to Database, do the following:

In Django project **Root** directory run command:
_$ python manage.py load_weather <weather_files_directory>_

**Note** that weather files must be of CSV format and name should follow this convention:

_CityName_weather_\<year>_\<month_abbr>.csv_


## Weatherman APIs

To get a year's weather, the URL is:
_<BASE_URL>/weather/yearly/\<year>/_

To get a month's average weather, the URL is:
_<BASE_URL>/weather/average-monthly/\<year>/\<month>/_
