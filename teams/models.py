from django.db import models
# Create your models here.
from teams.choices import BattingStyleChoices, BowlingStyleChoices, PlayingRoleChoices, FormatChoices


class Team(models.Model):
    name = models.CharField(max_length=50, default=' ')
    ranking = models.IntegerField(default=0)
    type = models.CharField(max_length=20, default='county')
    url = models.URLField(max_length=100, default=' ')

    def __str__(self):
        return self.name


class Player(models.Model):

    name = models.CharField(max_length=100, default=' ')
    DOB = models.DateTimeField('born')
    # Calculate Age
    playing_role = models.CharField(max_length=20, default=' ', choices=PlayingRoleChoices.Choices)
    batting_style = models.CharField(max_length=20, default=' ', choices=BattingStyleChoices.Choices)
    bowling_style = models.CharField(max_length=30, default=' ', choices=BowlingStyleChoices.Choices)
    major_teams = models.CharField(max_length=200, default=' ')
    ranking = models.PositiveSmallIntegerField(null=True, blank=True)
    url = models.URLField(max_length=100, default=' ')

    def __str__(self):
        return self.name


class BasicAverageIfo(models.Model):

    format = models.CharField(max_length=50, choices=FormatChoices.Choices)
    matches = models.IntegerField(null=True, blank=True)
    innings = models.IntegerField(null=True, blank=True)

    runs = models.IntegerField(null=True, blank=True)
    average = models.FloatField(null=True, blank=True)
    strike_rate = models.FloatField(null=True, blank=True)
    balls = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


class BattingAverage(BasicAverageIfo):

    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    not_outs = models.IntegerField(null=True, blank=True)
    highest_score = models.CharField(max_length=50, default=' ')    # 88*
    hundreds = models.IntegerField(null=True, blank=True)
    fifties = models.IntegerField(null=True, blank=True)
    fours = models.IntegerField(null=True, blank=True)
    sixes = models.IntegerField(null=True, blank=True)
    catches = models.IntegerField(null=True, blank=True)
    stumps = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{player_name}\'s batting average'.format(
            player_name=self.player
        )


class BowlingAverage(BasicAverageIfo):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    wickets = models.IntegerField(null=True, blank=True)
    best_bowling_innings = models.CharField(max_length=50, default=' ', null=True, blank=True)
    best_bowling_match = models.CharField(max_length=50, default=' ', null=True, blank=True)
    economy = models.FloatField(null=True, blank=True)
    four_wickets = models.IntegerField(null=True, blank=True)
    five_wickets = models.IntegerField(null=True, blank=True)
    ten_wickets = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{player_name}\'s bowling average'.format(
            player_name=self.player
        )


class Photos(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    photo_url = models.URLField(max_length=100, default=' ')

