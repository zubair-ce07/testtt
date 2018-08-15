from django.core.management.base import BaseCommand
import os
from teams.models import Player
import json


class Command(BaseCommand):
    help = 'loads the players data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['file_path']
        file_data = open(path[0]).read()
        player_data = json.loads(file_data)

        for player in player_data:
            print(player)