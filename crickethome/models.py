from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, default=' ')
    password = models.CharField(max_length=50, default=' ')
    type = models.CharField(max_length=50, default='simple')
    url = models.URLField(max_length=100, default=' ')


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


class Team(models.Model):
    name = models.CharField(max_length=50, default=' ')
    ranking = models.IntegerField(default=0)
    type = models.CharField(max_length=20, default='county')
    url = models.URLField(max_length=100, default=' ')


class Article(models.Model):
    title = models.CharField(max_length=100, default='Title')
    author = models.CharField(max_length=50, default='Author')
    description = models.CharField(max_length=100, default='Description')
    url = models.URLField(max_length=100, default=' ')


class BattingAverages(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_format = models.CharField(max_length=50, default=' ')
    matches = models.IntegerField(default=0)
    innings = models.IntegerField(default=0)
    not_outs = models.IntegerField(default=0)
    runs = models.IntegerField(default=0)
    highest_score = models.CharField(max_length=50, default=' ')  # 88*
    average = models.FloatField(default=0)
    balls_faced = models.IntegerField(default=0)
    strike_rate = models.FloatField(default=0)
    hundreds = models.IntegerField(default=0)
    fifties = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    sixes = models.IntegerField(default=0)
    catches = models.IntegerField(default=0)
    stumps = models.IntegerField(default=0)


class BowlingAverages(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    match_format = models.CharField(max_length=50, default=' ')
    matches = models.IntegerField(default=0)
    innings = models.IntegerField(default=0)
    balls = models.IntegerField(default=0)
    runs = models.IntegerField(default=0)
    wickets = models.IntegerField(default=0)
    best_bowling_innings = models.CharField(max_length=50, default=' ')
    best_bowling_match = models.CharField(max_length=50, default=' ')
    average = models.FloatField(default=0)
    economy = models.FloatField(default=0)
    strike_rate = models.FloatField(default=0)
    four_wickets = models.IntegerField(default=0)
    five_wickets = models.IntegerField(default=0)
    ten_wickets_in_match = models.IntegerField(default=0)


class PlayerComments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    player_id = models.ForeignKey(Player, default=0, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, default=' ')


class TeamComments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, default=0, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, default=' ')


class ArticleComments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Article, default=0, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200, default=' ')


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
    photo_url = models.URLField(max_length=100, default=' ')

