from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Glider)
admin.site.register(Airplane)
admin.site.register(AirplaneFlight)
admin.site.register(Chronometer)
admin.site.register(FuelPods)
admin.site.register(FuelTransactions)
admin.site.register(GliderTechnicalReview)
admin.site.register(AirplaneTechnicalReview)

