from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=50, default='s')
    url = models.URLField


class Player(models.Model):
    name = models.CharField
    DOB = models.DateTimeField('born')
    age = models.CharField(max_length=50)
    playing_role = models.CharField
    batting_style = models.CharField
    bowling_style = models.CharField
    major_team = models.CharField
    ranking = models.IntegerField
    url = models.URLField


class Team(models.Model):
    name = models.CharField
    ranking = models.IntegerField
    type = models.CharField(max_length=20, default='county')
    url = models.URLField


class Article(models.Model):
    title = models.CharField
    author = models.CharField
    description = models.CharField
    url = models.URLField


class BattingAverages(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_format = models.CharField
    matches = models.IntegerField
    innings = models.IntegerField
    not_outs = models.IntegerField
    runs = models.IntegerField
    highest_score = models.CharField  # 88*
    average = models.FloatField
    balls_faced = models.IntegerField
    strike_rate = models.FloatField
    hundreds = models.IntegerField
    fifties = models.IntegerField
    fours = models.IntegerField
    sixes = models.IntegerField
    catches = models.IntegerField
    stumps = models.IntegerField


class BowlingAverages(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_format = models.CharField
    matches = models.IntegerField
    innings = models.IntegerField
    balls = models.IntegerField
    runs = models.IntegerField
    wickets = models.IntegerField
    best_bowling_innings = models.CharField
    best_bowling_match = models.CharField
    average = models.FloatField
    economy = models.FloatField
    strike_rate = models.FloatField
    four_wickets = models.IntegerField
    five_wickets = models.IntegerField
    ten_wickets_in_match = models.IntegerField


class PlayerComments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, default=0, on_delete=models.CASCADE)
    comment_text = models.CharField


class TeamComments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, default=0, on_delete=models.CASCADE)
    comment_text = models.CharField


class ArticleComments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, default=0, on_delete=models.CASCADE)
    comment_text = models.CharField


class PlayerFollows(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, default=0, on_delete=models.CASCADE)


class TeamFollows(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, default=0, on_delete=models.CASCADE)


class ArticleFollows(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, default=0, on_delete=models.CASCADE)


class PlayerPhotos(models.Model):
    player_id = models.ForeignKey(Player, default=0, on_delete=models.CASCADE)
    photo_url = models.URLField
