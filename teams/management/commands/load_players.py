import argparse
from dateutil.parser import parse
import os
import sys
from django.core.management.base import BaseCommand
from teams.models import Player, Team, BattingAverage, BowlingAverage
import json
from datetime import datetime
from teams.choices import BattingStyleChoices, PlayingRoleChoices, FormatChoices, TeamTypeChoices, BOWLING_STYLES
import random


def get_player_name(player_data):
    try:
        return player_data.get('personal_info').get('Full name')[0]
    except TypeError or KeyError:
        return None


def get_player_dob(player_data):
    try:
        born = ''.join(((player_data.get('personal_info').get('Born')[0]).strip()).lstrip('\n').split(',')[:2])
        player_dob = datetime.strptime(born, '%B %d %Y').date()
    except ValueError or TypeError:
        player_dob = None
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
    found_teams = player_data.get('personal_info').get('Major teams')
    if found_teams:
        player_teams = [name.replace(',', '') for name in found_teams]
        for team in player_teams:
            team_instance = Team.objects.filter(name=team).first()
            if team_instance:
                player_teams_ids.append(team_instance.id)
    return player_teams_ids


def get_player_bowling_style(player_data):
    try:
        player_bowling_style = BOWLING_STYLES.get(player_data.get('personal_info').get('Bowling style')[0])
        if player_bowling_style is None:
            player_bowling_style = "NOT KNOWN"
    except TypeError or KeyError:
        return "NOT KNOWN"
    return player_bowling_style


def add_player_teams(team_ids, player):
    for i in team_ids:
        player.teams.add(i)


def empty_value_handler(average):
    for key in list(average.keys()):
        if average.get(key) == '' or average.get(key) == '-' or '+' in average.get(key):
            average[key] = None
        if average[key] and (key in ['Balls', 'Econ', 'SR']):
            average[key] = replace_handler(average[key])
    return average


def replace_handler(input_string):
    if '*' in input_string or '+' in input_string:
        input_string = input_string.replace('+', '')
        input_string = input_string.replace('*', '')
    return input_string


def create_player_batting_average(batting_data, player):
    for bat_avg in batting_data:
        bat_avg = empty_value_handler(bat_avg)
        batting_avg_instance, is_created = BattingAverage.objects.update_or_create(
            format=bat_avg[''].upper(), player_id=player.id,
            defaults={
                'format': bat_avg[''].upper(),
                'matches': bat_avg.get('Mat'),
                'innings': bat_avg.get('Inns'),
                'runs': bat_avg.get('Runs'),
                'average': bat_avg.get('Ave'),
                'strike_rate': bat_avg.get('SR'),
                'balls': bat_avg.get('BF'),
                'not_outs': bat_avg.get('NO'),
                'highest_score': bat_avg.get('HS'),
                'hundreds': bat_avg.get('100'),
                'fifties': bat_avg.get('50'),
                'fours': bat_avg.get('4s'),
                'sixes': bat_avg.get('6s'),
                'catches': bat_avg.get('Ct'),
                'stumps': bat_avg.get('St'),
                'player_id': player.id},
        )
        print(player.name + " batting average created" if is_created else player.name + " batting average updated")


def create_player_bowling_average(bowling_data, player):
    for bowl_avg in bowling_data:
        bowl_avg = empty_value_handler(bowl_avg)
        bowling_avg_instance, is_created = BowlingAverage.objects.update_or_create(
            format=bowl_avg[''].upper(), player_id=player.id,
            defaults={
                'format': bowl_avg[''].upper(),
                'matches': bowl_avg.get('Mat'),
                'innings': bowl_avg.get('Inns'),
                'runs': bowl_avg.get('Runs'),
                'average': bowl_avg.get('Ave'),
                'strike_rate': bowl_avg.get('SR'),
                'balls': bowl_avg.get('Balls'),
                'wickets': bowl_avg.get('Wkts'),
                'best_bowling_innings': bowl_avg.get('BBI'),
                'best_bowling_match': bowl_avg.get('BBM'),
                'economy': bowl_avg.get('Econ'),
                'four_wickets': bowl_avg.get('4w'),
                'five_wickets': bowl_avg.get('5w'),
                'ten_wickets': bowl_avg.get('10'),
                'player_id': player.id},
        )
        print(player.name + " bowling average created" if is_created else player.name + " bowling average updated")


def create_player(player_data):
    if get_player_name(player_data) and get_player_dob(player_data):
        player_instance, is_created = Player.objects.update_or_create(
            name=get_player_name(player_data),
            defaults={'name': get_player_name(player_data), 'DOB': get_player_dob(player_data),
                      'playing_role': get_player_role(player_data), 'batting_style': get_player_batting_style(player_data),
                      'bowling_style': get_player_bowling_style(player_data)}
        )
        print(get_player_name(player_data) + " created" if is_created else get_player_name(player_data) + " updated")
        return player_instance, is_created
    else:
        return [None, False]


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
                if player_instance:
                    add_player_teams(player_teams_ids, player_instance)
                    create_player_batting_average(batting_data, player_instance)
                    create_player_bowling_average(bowling_data, player_instance)
