""" This is a custom management to show current orders. """

import csv
from datetime import date

from django.core.management.base import BaseCommand
from users.models import Order, OrderItems

def order_report():
    """ It print orders of current date into file. """
    curr_date = str(date.today())
    filename = f'{curr_date}.csv'
    with open(filename, 'w') as file_open:
        report = csv.DictWriter(file_open, fieldnames=['name', 'city', 'item'])
        report.writeheader()
        for order in Order.objects.filter(order_date=date.today()):
            item = list(OrderItems.objects.filter(order_id=int(order.id)) \
                .values_list('product_id', 'quantity'))
            report.writerows([{'name': order.name, 'city': order.city, 'item': str(item)}])

class Command(BaseCommand):
    """ Our custom command class extracted from Base Commands. """

    def handle(self, **options):
        """ This function calls on command invoke. """
        order_report()
