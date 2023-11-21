# Generated by Django 4.2.7 on 2023-11-21 13:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_flight_end_date_alter_flight_start_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='end_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_flights', to='main.city'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='start_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_flights', to='main.city'),
        ),
        migrations.AlterField(
            model_name='stay',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 21, 13, 30, 44, 982914)),
        ),
        migrations.AlterField(
            model_name='stay',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 21, 13, 30, 44, 982904)),
        ),
    ]
