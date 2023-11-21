# Generated by Django 4.2.7 on 2023-11-21 12:58

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_remove_stay_stay_dict_stay_stay_adults_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='end_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='end_flights', to='main.location'),
        ),
        migrations.AddField(
            model_name='flight',
            name='flight_category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='flight',
            name='start_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='start_flights', to='main.location'),
        ),
        migrations.AlterField(
            model_name='flight',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='flight',
            name='start_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='stay',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 21, 12, 58, 9, 766330, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='stay',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 21, 12, 58, 9, 766310, tzinfo=datetime.timezone.utc)),
        ),
    ]
