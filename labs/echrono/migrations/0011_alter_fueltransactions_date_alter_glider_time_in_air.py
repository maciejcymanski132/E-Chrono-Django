# Generated by Django 4.0.4 on 2022-06-19 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('echrono', '0010_alter_chronometer_airplane_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fueltransactions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 22, 26, 24, 900117)),
        ),
        migrations.AlterField(
            model_name='glider',
            name='time_in_air',
            field=models.IntegerField(blank=True, null=True, verbose_name='time_in_air'),
        ),
    ]
