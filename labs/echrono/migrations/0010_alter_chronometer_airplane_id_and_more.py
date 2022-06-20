# Generated by Django 4.0.4 on 2022-06-19 18:24

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('echrono', '0009_alter_chronometer_airplane_landing_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chronometer',
            name='airplane_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='echrono.airplane'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='instructor_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='instruct', to='echrono.user'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='tow_pilot_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='tow', to='echrono.user'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='winch_operator_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winch', to='echrono.user'),
        ),
        migrations.AlterField(
            model_name='fueltransactions',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 20, 24, 5, 854481)),
        ),
    ]