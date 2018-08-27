# Generated by Django 2.0.7 on 2018-08-27 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20180827_1043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='DOB',
            field=models.DateField(blank=True, null=True, verbose_name='Born'),
        ),
        migrations.AlterField(
            model_name='player',
            name='batting_style',
            field=models.CharField(blank=True, choices=[('RIGHT_HANDED', 'Right Hand Bat'), ('LEFT_HANDED', 'Left Hand Bat')], default=' ', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='bowling_style',
            field=models.CharField(blank=True, choices=[('RIGHT_ARM_FAST', 'Right Arm Fast'), ('RIGHT_ARM_MEDIUM_FAST', 'Right Arm Medium Fast'), ('RIGHT_ARM_OFF_BREAK', 'Right Arm OffBreak'), ('RIGHT_ARM_LEG_BREAK_GOOGLY', 'Right Arm LegBreak Googly'), ('RIGHT_ARM_ORTHODOX', 'Right Arm Orthodox'), ('RIGHT_ARM_SLOW', 'Right Arm Slow'), ('LEFT_ARM_FAST', 'Left Arm Fast'), ('LEFT_ARM_MEDIUM_FAST', 'Left Arm Medium Fast'), ('LEFT_ARM_ORTHODOX', 'Left Arm Orthodox'), ('LEFT_ARM_CHINAMAN', 'Left Arm Chinaman'), ('LEFT_ARM_SLOW', 'Left Arm Slow')], default=' ', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='playing_role',
            field=models.CharField(blank=True, choices=[('BATSMAN', 'Batsman'), ('BOWLER', 'Bowler'), ('ALLROUNDER', 'AllRounder'), ('WICKETKEEPER', 'WicketKeeper')], default=' ', max_length=20, null=True),
        ),
    ]
