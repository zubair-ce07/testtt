NewsRoom
=======

The purpose of this repo is to help the team lead and his team members to develop a news website which will fetch news from different websites and also provide analytics for its users

## Scrum Master
Verdan Mahmood

## Developers

1. Luqman-Ud-Din Muhammad
1. Rayyan Khalid


## How to run

- Install all packages mentioned in requirements.txt
- Run Django Server 
  - python manage.py runserver
- Run 'memcached' for Django Caching framework by typing in terminal 'memcached'
- Run RabbitMQ service
- Run Celery 
  - celery -A newsroom worker --beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler

