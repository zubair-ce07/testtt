from django.db import models

# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=100, default=' ')
    born = models.DateTimeField('born')
    age = models.CharField(max_length=50, default=' ')
    playing_role = models.CharField(max_length=50, default=' ')
    batting_style = models.CharField(max_length=50, default=' ')
    bowling_style = models.CharField(max_length=50, default=' ')
    major_team = models.CharField(max_length=200, default=' ')
    ranking = models.IntegerField(default=0)
    url = models.URLField(max_length=100, default=' ')

    def __str__(self):
        return self.name


class BattingAverage(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_format = models.CharField(max_length=50, default=' ')
    matches = models.IntegerField
    innings = models.IntegerField
    not_outs = models.IntegerField
    runs = models.IntegerField
    highest_score = models.CharField(max_length=50, default=' ')  # 88*
    average = models.FloatField(default=0)
    balls_faced = models.IntegerField
    strike_rate = models.FloatField(default=0)
    hundreds = models.IntegerField
    fifties = models.IntegerField
    fours = models.IntegerField
    sixes = models.IntegerField
    catches = models.IntegerField
    stumps = models.IntegerField


class BowlingAverage(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_format = models.CharField(max_length=50, default=' ')
    matches = models.IntegerField
    innings = models.IntegerField
    balls = models.IntegerField
    runs = models.IntegerField
    wickets = models.IntegerField
    best_bowling_innings = models.CharField(max_length=50, default=' ')
    best_bowling_match = models.CharField(max_length=50, default=' ')
    average = models.FloatField(default=0)
    economy = models.FloatField(default=0)
    strike_rate = models.FloatField(default=0)
    four_wickets = models.IntegerField
    five_wickets = models.IntegerField
    ten_wickets = models.IntegerField


class PlayerPhotos(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    photo_url = models.URLField(max_length=100, default=' ')

