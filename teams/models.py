from django.db import models
from model_utils import Choices

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=50, default=' ')
    ranking = models.IntegerField(default=0)
    type = models.CharField(max_length=20, default='county')
    url = models.URLField(max_length=100, default=' ')

    def __str__(self):
        return self.name


class Player(models.Model):
    PLAYING_ROLES = Choices(
        ('batsman', 'Batsman'),
        ('bowler', 'Bowler'),
        ('allrounder', 'AllRounder'),
        ('wicketkeeper', 'WicketKeeper'),
    )
    BATTING_STYLES = Choices(
        ('right-hand', 'Right Hand Bat'),
        ('left-hand', 'Left Hand Bat'),
    )
    BOWLING_STYLES = Choices(
        ('right-arm-fast', 'Right Arm Fast'),
        ('right-arm-medium-fast', 'Right Arm Medium Fast'),
        ('right-arm-off-break', 'Right Arm OffBreak'),
        ('right-arm-leg-break-googly', 'Right Arm LegBreak Googly'),
        ('right-arm-orthodox', 'Right Arm Orthodox'),
        ('left-arm-fast', 'Left Arm Fast'),
        ('left-arm-medium-fast', 'Left Arm Medium Fast'),
        ('left-arm-orthodox', 'Left Arm Orthodox'),
        ('left-arm-chinaman', 'Left Arm Chinaman'),
    )
    name = models.CharField(max_length=100, default=' ')
    DOB = models.DateTimeField('born')
    # Calculate Age
    playing_role = models.CharField(max_length=20, default=' ', choices=PLAYING_ROLES)
    batting_style = models.CharField(max_length=20, default=' ', choices=BATTING_STYLES)
    bowling_style = models.CharField(max_length=30, default=' ', choices=BOWLING_STYLES)
    major_teams = models.CharField(max_length=200, default=' ')
    ranking = models.PositiveSmallIntegerField(null=True, blank=True)
    url = models.URLField(max_length=100, default=' ')

    def __str__(self):
        return self.name


class BasicAverageIfo(models.Model):
    FORMATS = Choices(
        ('test', 'Tests'),
        ('odi', 'ODIs'),
        ('t20i', 'T20Is'),
        ('first-class', 'FirstClass'),
        ('list A', 'ListA'),
        ('t20', 'T20s'),
    )
    format = models.CharField(max_length=50, choices=FORMATS)
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
    # TODO: Limit this to specific choices

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

