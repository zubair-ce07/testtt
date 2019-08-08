# Generated by Django 2.1.7 on 2019-04-16 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contents',
            name='status',
            field=models.IntegerField(choices=[(1, 'Not relevant'), (2, 'Review'), (3, 'Maybe relevant'), (4, 'Relevant'), (5, 'Leading candidate')], default=1),
        ),
        migrations.AddField(
            model_name='contents',
            name='user_id',
            field=models.IntegerField(default=0),
        ),
    ]
