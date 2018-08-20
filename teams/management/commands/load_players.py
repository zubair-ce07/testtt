import argparse
from dateutil.parser import parse
import os
import sys
from django.core.management.base import BaseCommand
from teams.models import Player, Team, BattingAverage, BowlingAverage
import json
from datetime import datetime
from teams.choices import BattingStyleChoices, BowlingStyleChoices, PlayingRoleChoices, FormatChoices, TeamTypeChoices
import random


def get_player_name(player_data):
    return player_data.get('personal_info').get('Full name')[0]


def get_player_dob(player_data):
    born = ''.join(((player_data.get('personal_info').get('Born')[0]).strip()).lstrip('\n').split(',')[:2])
    player_dob = datetime.strptime(born, '%B %d %Y').date()
    return player_dob


def get_player_role(player_data):
    try:
        role = (player_data.get('personal_info').get('Playing role')[0].upper()).split(' ')
    except TypeError or KeyError:
        return "BATSMAN"
    return 'WICKETKEEPER' if 'WICKETKEEPER' in role else role[-1]


def get_player_batting_style(player_data):
    batting_style = player_data.get('personal_info').get('Batting style')[0].split(' ')
    return BattingStyleChoices.RIGHT_HAND if batting_style[0] == 'Right-hand' else BattingStyleChoices.LEFT_HAND


def get_player_teams_ids(player_data):
    player_teams_ids = []
    player_teams = [name.replace(',', '') for name in player_data.get('personal_info').get('Major teams')]
    for team in player_teams:
        team_instance = Team.objects.filter(name=team).first()
        if team_instance:
            player_teams_ids.append(team_instance.id)
    return player_teams_ids


BOWLING_STYLES = {
                'Right-arm fast': BowlingStyleChoices.RIGHT_ARM_FAST,
                'Right-arm fast-medium': BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST,
                'Right-arm medium-fast': BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST,
                'Right-arm medium': BowlingStyleChoices.RIGHT_ARM_MEDIUM_FAST,
                'Right-arm offbreak': BowlingStyleChoices.RIGHT_ARM_OFF_BREAK,
                'Legbreak googly': BowlingStyleChoices.RIGHT_ARM_LEG_BREAK_GOOGLY,
                'Left-arm fast': BowlingStyleChoices.LEFT_ARM_FAST,
                'Left-arm fast-medium': BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST,
                'Left-arm medium-fast': BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST,
                'Left-arm medium': BowlingStyleChoices.LEFT_ARM_MEDIUM_FAST,
                'Slow left-arm chinaman': BowlingStyleChoices.LEFT_ARM_CHINAMAN,
                'Slow left-arm orthodox': BowlingStyleChoices.LEFT_ARM_ORTHODOX,
                'Legbreak': BowlingStyleChoices.RIGHT_ARM_LEG_BREAK_GOOGLY
}


def get_player_bowling_style(player_data):
    try:
        if 'personal_info' in player_data and 'Bowling style' in player_data:
            player_bowling_style = BOWLING_STYLES.get(player_data['personal_info']['Bowling style'][0])
        else:
            return "NOT KNOWN"
    except TypeError or KeyError:
        return "NOT KNOWN"

    return player_bowling_style


def add_player_teams(team_ids, player):
    for i in team_ids:
        player.teams.add(i)


def create_player_batting_average(batting_data, player):
    for bat_avg in batting_data:
        batting_avg_instance, is_created = BattingAverage.objects.update_or_create(
            format=bat_avg[''].upper(), player_id=player.id,
            defaults={'format': bat_avg[''].upper(), 'matches': int(bat_avg['Mat']), 'innings': int(bat_avg['Inns']),
                      'runs': int(bat_avg['Runs']), 'average': float(bat_avg['Ave']), 'strike_rate': float(bat_avg['SR']),
                      'balls': int(bat_avg['BF']), 'not_outs': int(bat_avg['NO']), 'highest_score': (bat_avg['HS']),
                      'hundreds': int(bat_avg['100']), 'fifties': int(bat_avg['50']), 'fours': int(bat_avg['4s']),
                      'sixes': int(bat_avg['6s']), 'catches': int(bat_avg['Ct']), 'stumps': int(bat_avg['St']),
                      'player_id': player.id},
        )
        print(player.name + " batting average created" if is_created else player.name + " batting average updated")


def create_player_bowling_average(bowling_data, player):
    for bowl_avg in bowling_data:
        bowling_avg_instance, is_created = BowlingAverage.objects.update_or_create(
            format=bowl_avg[''].upper(), player_id=player.id,
            defaults={'format': bowl_avg[''].upper(), 'matches': int(bowl_avg['Mat']), 'innings': int(bowl_avg['Inns']),
                      'runs': int(bowl_avg['Runs']), 'average': float(bowl_avg['Ave']),
                      'strike_rate': float(bowl_avg['SR']), 'balls': int(bowl_avg['Balls']),
                      'wickets': int(bowl_avg['Wkts']), 'best_bowling_innings': (bowl_avg['BBI']),
                      'best_bowling_match': (bowl_avg['BBM']), 'economy': float(bowl_avg['Econ']),
                      'four_wickets': int(bowl_avg['4w']), 'five_wickets': int(bowl_avg['5w']),
                      'ten_wickets': int(bowl_avg['10']),
                      'player_id': player.id},
        )
        print(player.name + " bowling average created" if is_created else player.name + " bowling average updated")


def create_player(player_data):

    player_instance, is_created = Player.objects.update_or_create(
        name=get_player_name(player_data),
        defaults={'name': get_player_name(player_data), 'DOB': get_player_dob(player_data),
                  'playing_role': get_player_role(player_data), 'batting_style': get_player_batting_style(player_data),
                  'bowling_style': get_player_bowling_style(player_data)}
    )

    print(get_player_name(player_data) + " created" if is_created else get_player_name(player_data) + " updated")
    return player_instance, is_created


class Command(BaseCommand):
    help = 'loads the players data'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str, action='store')

    def handle(self, *args, **options):
        path = options['file_path']
        all_players_files = os.listdir(path[0])
        dir_path = '/home/raziullah/Desktop/BackupFolder/PlayersJSONFiles/'
        for player_file in all_players_files:
            with open(dir_path + player_file) as file_obj:
                file_data = file_obj.read()
                player_data = json.loads(file_data)
                batting_data = player_data.get('batting_averages')
                bowling_data = player_data.get('bowling_averages')
                player_teams_ids = get_player_teams_ids(player_data)

                player_instance, is_created = create_player(player_data)

                add_player_teams(player_teams_ids, player_instance)
                create_player_batting_average(batting_data, player_instance)
                create_player_bowling_average(batting_data, player_instance)
