# Generated by Django 4.2.7 on 2023-11-15 04:30

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_city_country_flight_location_stay_city_country_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stay',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
