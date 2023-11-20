# Generated by Django 4.2.7 on 2023-11-20 11:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_stay_end_date_alter_stay_start_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stay',
            name='stay_dict',
        ),
        migrations.AddField(
            model_name='stay',
            name='stay_Adults',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='stay',
            name='stay_Children',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='stay',
            name='stay_Room',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='stay',
            name='end_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 20, 11, 42, 25, 926902)),
        ),
        migrations.AlterField(
            model_name='stay',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 11, 20, 11, 42, 25, 926893)),
        ),
    ]