# Generated by Django 4.0.4 on 2022-06-15 06:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('echrono', '0004_fuelpods_fill_percentage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chronometer',
            name='airplane_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='airplane', to='echrono.airplane'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='glider_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='glider_id', to='echrono.glider'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='instructor_id',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='instructor_id', to='echrono.user'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='pilot_passenger_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pilot_id', to='echrono.user'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='tow_pilot_id',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='tow_pilot', to='echrono.user'),
        ),
        migrations.AlterField(
            model_name='chronometer',
            name='winch_operator_id',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.DO_NOTHING, related_name='winch_operator_id', to='echrono.user'),
        ),
    ]