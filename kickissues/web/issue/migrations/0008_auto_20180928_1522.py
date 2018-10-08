# Generated by Django 2.1.1 on 2018-09-28 10:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0007_auto_20180927_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='manage_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_issues', to=settings.AUTH_USER_MODEL),
        ),
    ]
