# Generated by Django 4.0.4 on 2022-06-19 20:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('echrono', '0011_alter_fueltransactions_date_alter_glider_time_in_air'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airplane',
            name='time_in_air',
            field=models.IntegerField(blank=True, null=True, verbose_name='time_in_air'),
        ),
        migrations.AlterField(
            model_name='fueltransactions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 22, 26, 56, 24401)),
        ),
    ]