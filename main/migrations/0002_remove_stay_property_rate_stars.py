# Generated by Django 4.2.7 on 2023-11-28 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stay',
            name='property_rate_stars',
        ),
    ]
