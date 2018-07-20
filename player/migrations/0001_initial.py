# Generated by Django 2.2.dev20180707212002 on 2018-07-20 14:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BattingAverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_format', models.CharField(default=' ', max_length=50)),
                ('highest_score', models.CharField(default=' ', max_length=50)),
                ('average', models.FloatField(default=0)),
                ('strike_rate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='BowlingAverage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_format', models.CharField(default=' ', max_length=50)),
                ('best_bowling_innings', models.CharField(default=' ', max_length=50)),
                ('best_bowling_match', models.CharField(default=' ', max_length=50)),
                ('average', models.FloatField(default=0)),
                ('economy', models.FloatField(default=0)),
                ('strike_rate', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=' ', max_length=100)),
                ('born', models.DateTimeField(verbose_name='born')),
                ('age', models.CharField(default=' ', max_length=50)),
                ('playing_role', models.CharField(default=' ', max_length=50)),
                ('batting_style', models.CharField(default=' ', max_length=50)),
                ('bowling_style', models.CharField(default=' ', max_length=50)),
                ('major_team', models.CharField(default=' ', max_length=200)),
                ('ranking', models.IntegerField(default=0)),
                ('url', models.URLField(default=' ', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerPhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url', models.URLField(default=' ', max_length=100)),
                ('player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player')),
            ],
        ),
        migrations.AddField(
            model_name='bowlingaverage',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player'),
        ),
        migrations.AddField(
            model_name='battingaverage',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='player.Player'),
        ),
    ]
