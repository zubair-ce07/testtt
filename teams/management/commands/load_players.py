import argparse
from dateutil.parser import parse
import os
from django.core.management.base import BaseCommand
from teams.models import Player, Team, BattingAverage, BowlingAverage
import json
from datetime import datetime
from teams.choices import BattingStyleChoices, BowlingStyleChoices, PlayingRoleChoices, FormatChoices, TeamTypeChoices
import random


class Command(BaseCommand):
    help = 'loads the players data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str, action='store')

    def handle(self, *args, **options):
        path = options['file_path']
        file_data = open(path[0]).read()
        player_data = json.loads(file_data)

        player_name = player_data['personal_info']['Full name'][0]
        born = (((player_data['personal_info']['Born'][0]).strip()).lstrip('\n').rsplit(',', 1)[0])
        player_dob = datetime.strptime(born, '%B %d, %Y').date()
        role = player_data['personal_info']['Playing role'][0].upper()
        role = role.split(' ')
        if role[0] == 'WICKETKEEPER':
            player_role = role[0]
        else:
            player_role = role[1]

        batting_style = player_data['personal_info']['Batting style'][0].split(' ')
        if batting_style[0] == 'Right-hand':
            player_batting_style = BattingStyleChoices.RIGHT_HAND
        else:
            player_batting_style = BattingStyleChoices.LEFT_HAND

        player_bowling_style = ''
        bowling_style = player_data['personal_info']['Bowling style'][0].split(' ')
        if bowling_style[0] == 'Right-arm':
            if any("medium" in s for s in bowling_style):
                player_bowling_style = BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST
            elif any("fast" in s for s in bowling_style):
                player_bowling_style = BowlingStyleChoices.RIGHT_ARM_FAST
            elif any("offbreak" in s for s in bowling_style):
                player_bowling_style = BowlingStyleChoices.RIGHT_ARM_OFF_BREAK
            elif any("orthdox" in s for s in bowling_style):
                player_bowling_style = BowlingStyleChoices.RIGHT_ARM_ORTHODOX
            elif any("slow" in s for s in bowling_style):
                player_bowling_style = 'RIGHT ARM SLOW'
        elif bowling_style[0] == 'Left-arm':
            if any("medium" in s for s in bowling_style):
                player_bowling_style = BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST
            elif any("fast" in s for s in bowling_style):
                player_bowling_style = BowlingStyleChoices.LEFT_ARM_FAST
            elif any("orthdox" in s for s in bowling_style):
                player_bowling_style = BowlingStyleChoices.LEFT_ARM_ORTHODOX
        elif bowling_style[0] == 'Legbreak':
            player_bowling_style = BowlingStyleChoices.RIGHT_ARM_LEG_BREAK_GOOGLY
        elif any("chinaman" in s for s in bowling_style):
            player_bowling_style = BowlingStyleChoices.LEFT_ARM_CHINAMAN

        player_teams = (player_data['personal_info']['Major teams'][0]).rstrip(',')
        team = Team.objects.get(name=player_teams)
        team_id = team.id

        random.seed(datetime.now())

        player_instance = Player.objects.create(
            name=player_name,
            DOB=player_dob,
            playing_role=player_role,
            batting_style=player_batting_style,
            bowling_style=player_bowling_style,
            ranking=random.randint(1, 101)
        )
        player_instance.teams.add(team_id)

        batting_data = player_data['batting_averages']
        for bat_avg in batting_data:
            pass
            # batting_avg_instance = BattingAverage.objects.create(
            #     format=list(bat_avg.values())[0],
            #     matches=list(bat_avg.values())[0]
            # )

        # print(player_data['batting_averages'][0]['Mat'])
        # for player in player_data:
        #     print(player)
        print('bla')
        # Player.objects.get_or_create(
        #     name=player_name,
        #     playing_role="Batsman",
        # )
