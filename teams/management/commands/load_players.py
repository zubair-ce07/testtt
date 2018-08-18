import argparse
from dateutil.parser import parse
import os
from django.core.management.base import BaseCommand
from teams.models import Player, Team, BattingAverage, BowlingAverage
import json
from datetime import datetime
from teams.choices import BattingStyleChoices, BowlingStyleChoices, PlayingRoleChoices, FormatChoices, TeamTypeChoices
import random


def get_player_name(player_data):
    return player_data['personal_info']['Full name'][0]


def get_player_dob(player_data):
    born = ((player_data['personal_info']['Born'][0]).strip()).lstrip('\n').rsplit(',', 1)[0]
    player_dob = datetime.strptime(born, '%B %d, %Y').date()
    return player_dob


def get_player_role(player_data):
    role = (player_data['personal_info']['Playing role'][0].upper()).split(' ')
    if role[0] == 'WICKETKEEPER':
        player_role = role[0]
    else:
        player_role = role[1]
    return player_role


def get_player_batting_style(player_data):
    batting_style = player_data['personal_info']['Batting style'][0].split(' ')
    if batting_style[0] == 'Right-hand':
        player_batting_style = BattingStyleChoices.RIGHT_HAND
    else:
        player_batting_style = BattingStyleChoices.LEFT_HAND
    return player_batting_style


def get_player_teams_ids(player_data):
    player_teams = player_data['personal_info']['Major teams']
    player_teams = [name[:-1] for name in player_teams if name.endswith(',')]
    player_teams_ids = []
    for team in player_teams:
        team_instance = Team.objects.filter(name=team)
        if team_instance:
            team_id = team_instance[0].id
            player_teams_ids.append(team_id)
    return player_teams_ids


def get_player_bowling_style(player_data):
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

    return player_bowling_style


class Command(BaseCommand):
    help = 'loads the players data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str, action='store')

    def handle(self, *args, **options):
        path = options['file_path']
        file_data = open(path[0]).read()
        player_data = json.loads(file_data)
        batting_data = player_data['batting_averages']
        bowling_data = player_data['bowling_averages']

        player_name = get_player_name(player_data)
        player_dob = get_player_dob(player_data)
        player_role = get_player_role(player_data)
        player_batting_style = get_player_batting_style(player_data)
        player_bowling_style = get_player_bowling_style(player_data)
        player_teams_ids = get_player_teams_ids(player_data)
        random.seed(datetime.now())

        player_instance, is_created = Player.objects.update_or_create(
            name=player_name, DOB=player_dob, playing_role=player_role, batting_style=player_batting_style,
            bowling_style=player_bowling_style, ranking=random.randint(1, 101),
            defaults={'name': player_name, 'DOB': player_dob, 'playing_role': player_role,
                      'batting_style': player_batting_style, 'bowling_style': player_bowling_style,
                      'ranking': random.randint(1, 101)}
        )

        for bat_avg in batting_data:
            batting_avg_instance, is_created = BattingAverage.objects.update_or_create(
                format=bat_avg[''].upper(), matches=int(bat_avg['Mat']), innings=int(bat_avg['Inns']),
                runs=int(bat_avg['Runs']), average=float(bat_avg['Ave']), strike_rate=float(bat_avg['SR']),
                balls=int(bat_avg['BF']), not_outs=int(bat_avg['NO']), highest_score=(bat_avg['HS']),
                hundreds=int(bat_avg['100']), fifties=int(bat_avg['50']), fours=int(bat_avg['4s']),
                sixes=int(bat_avg['6s']), catches=int(bat_avg['Ct']), stumps=int(bat_avg['St']),
                player_id=player_instance.id
            )

        for bowl_avg in bowling_data:
            bowling_avg_instance, is_created = BowlingAverage.objects.update_or_create(
                format=bowl_avg[''].upper(), matches=int(bowl_avg['Mat']), innings=int(bowl_avg['Inns']),
                runs=int(bowl_avg['Runs']), average=float(bowl_avg['Ave']), strike_rate=float(bowl_avg['SR']),
                balls=int(bowl_avg['Balls']), wickets=int(bowl_avg['Wkts']), best_bowling_innings=bowl_avg['BBI'],
                best_bowling_match=bowl_avg['BBM'], economy=float(bowl_avg['Econ']), four_wickets=int(bowl_avg['4w']),
                five_wickets=int(bowl_avg['5w']), ten_wickets=int(bowl_avg['10']),
                player_id=player_instance.id
            )

        for i in player_teams_ids:
            player_instance.teams.add(i)
