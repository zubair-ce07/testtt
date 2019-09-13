# Generated by Django 2.2.5 on 2019-09-13 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20190912_1118'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favoriter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='upload_favoriter', to='portal.Profile')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Profile')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Uploads')),
            ],
        ),
    ]
