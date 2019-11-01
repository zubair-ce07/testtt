from django.core.management.base import BaseCommand
from users.models import Order
from datetime import date

import csv

def add_dummy_data():
    filename = str(date.today())+'.txt'
    with open(filename, 'w') as report:
        for order in Order.objects.filter(order_date=date.today()):
            report.write(order.name +',' + order.city +','+ order.phone +'\n')

class Command(BaseCommand):
    def handle(self, **options):
        add_dummy_data()