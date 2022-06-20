from datetime import datetime

from django.db import models


class User(models.Model):
    __tablename__ = "user"

    firstname = models.CharField("firstname", max_length=30, blank=False)
    lastname = models.CharField("lastname", max_length=30, blank=False)
    instructor = models.BooleanField("instructor", default=False)
    winch_operator = models.BooleanField("winch_operator", default=False)
    glider_pilot = models.BooleanField("glider_pilot", default=False)
    airplane_pilot = models.BooleanField("airplane_pilot", default=False)
    inspector = models.BooleanField("inspector", default=False)


class Glider(models.Model):
    __tablename__ = "glider"

    name = models.CharField("name", max_length=10, blank=False)
    time_in_air = models.IntegerField("time_in_air", blank=True, null=True)


class Airplane(models.Model):
    __tablename__ = "airplane"

    name = models.CharField("name", max_length=10, blank=False)
    time_in_air = models.IntegerField("time_in_air", blank=True, null=True)


class Chronometer(models.Model):
    __tablename__ = "chrono"

    time_of_start = models.DateTimeField("time_of_start", null=True)
    glider_landing_time = models.DateTimeField("glider_landing_time", null=True)
    airplane_landing_time = models.DateTimeField("airplane_landing_time", null=True)
    glider_tia = models.CharField("glider_tia", null=True, default="-", max_length=15)
    airplane_tia = models.CharField("glider_tia", null=True, default="-", max_length=15)
    start_type = models.CharField("start_type", max_length=1, blank=False)
    active = models.BooleanField("active", default=False)

    winch_operator_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, default='',
                                          related_name='winch', null=True)
    tow_pilot_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, default='', related_name='tow',
                                     null=True)
    instructor_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, default='',
                                      related_name='instruct', null=True)
    pilot_passenger_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, default='pilot')
    glider_id = models.ForeignKey(Glider, on_delete=models.DO_NOTHING)
    airplane_id = models.ForeignKey(Airplane, on_delete=models.DO_NOTHING, null=True)


class AirplaneFlight(models.Model):
    __tablename__ = "airplaneflight"

    time_of_start = models.DateTimeField()

    airplane_pilot = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    airplane = models.ForeignKey(Airplane, on_delete=models.DO_NOTHING)


class AirplaneTechnicalReview(models.Model):
    __tablename__ = "airplanereview"

    date = models.DateTimeField()
    inspector_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    airplane_id = models.ForeignKey(Airplane, on_delete=models.DO_NOTHING)
    engine_check = models.BooleanField()
    fuselage_check = models.BooleanField()
    sheathing_check = models.BooleanField()


class GliderTechnicalReview(models.Model):
    __tablename__ = "gliderreview"

    date = models.DateTimeField()
    inspector_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    glider_id = models.ForeignKey(Glider, on_delete=models.DO_NOTHING)
    wings_check = models.BooleanField(default=False)
    fuselage_check = models.BooleanField(default=False)
    sheathing_check = models.BooleanField(default=False)


class FuelPods(models.Model):
    __tablename__ = "FuelPods"

    capacity = models.IntegerField()
    fill_level = models.FloatField()
    fill_percentage = models.IntegerField(default=100)


class FuelTransactions(models.Model):
    __tablename__ = "substitutes"

    buyer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    quantity = models.FloatField()
    aircraft_id = models.ForeignKey(Airplane, on_delete=models.DO_NOTHING)
    fuel_pod = models.ForeignKey(FuelPods, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(default=datetime.now())
