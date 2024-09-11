# Generated by Django 5.1.1 on 2024-09-08 21:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ElectricityData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(db_index=True, max_length=255)),
                ('state', models.CharField(db_index=True, max_length=255)),
                ('date', models.DateField(db_index=True)),
                ('region', models.CharField(db_index=True, max_length=255)),
                ('NOK_per_kWh', models.FloatField()),
                ('EUR_per_kWh', models.FloatField()),
                ('EXR', models.FloatField()),
                ('time_start', models.CharField(max_length=255)),
                ('time_end', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'electricity_prices',
                'indexes': [models.Index(fields=['city'], name='electricity_city_a298fc_idx'), models.Index(fields=['state'], name='electricity_state_7f148e_idx'), models.Index(fields=['date'], name='electricity_date_712739_idx'), models.Index(fields=['region'], name='electricity_region_3e656b_idx')],
            },
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(db_index=True, max_length=255)),
                ('state', models.CharField(db_index=True, max_length=255)),
                ('date', models.DateField(db_index=True)),
                ('temperature', models.FloatField()),
                ('time_start', models.CharField(max_length=255)),
                ('time_end', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'db_table': 'weather_data',
                'indexes': [models.Index(fields=['city'], name='weather_dat_city_96d319_idx'), models.Index(fields=['state'], name='weather_dat_state_c41749_idx'), models.Index(fields=['date'], name='weather_dat_date_b3710c_idx')],
            },
        ),
    ]
