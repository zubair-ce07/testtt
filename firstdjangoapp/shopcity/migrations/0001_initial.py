from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('retailer_sku', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('brand', models.CharField(blank=True, max_length=50)),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar'), ('GBP', 'Great Britain Pound')], max_length=10)),
                ('price', models.IntegerField()),
                ('url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('image_url', models.TextField()),
                ('care', models.TextField(blank=True)),
                ('gender', models.CharField(choices=[('women', 'women'), ('men', 'men'), ('girls', 'girls'), ('boys', 'boys'), ('unisex-kids', 'unisex-kids'), ('unisex-adults', 'unisex-adults')], max_length=20)),
                ('out_of_stock', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Skus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.CharField(max_length=50)),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar'), ('GBP', 'Great Britain Pound')], max_length=20)),
                ('colour', models.CharField(blank=True, max_length=20)),
                ('price', models.IntegerField()),
                ('size', models.CharField(blank=True, max_length=20)),
                ('previous_prices', models.TextField(blank=True)),
                ('out_of_stock', models.BooleanField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skus', to='shopcity.Product')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=20)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='shopcity.Product')),
            ],
        ),
    ]
