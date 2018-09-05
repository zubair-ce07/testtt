from django.core.management.base import BaseCommand
from teams.models import Player, Team
import json


class Command(BaseCommand):
    help = 'loads the teams data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str, action='store')

    def handle(self, *args, **options):
        path = options['file_path']
        file_data = open(path[0]).read()
        teams_data = json.loads(file_data)
        all_teams = teams_data['teams']
        for team in all_teams:
            Team.objects.create(name=team['name'], ranking=team['ranking'], type=team['type'])
