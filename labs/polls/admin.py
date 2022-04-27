from django.contrib import admin

from .models import *

admin.site.register(Book)
admin.site.register(Provider)
admin.site.register(Author)
admin.site.register(Customer)
admin.site.register(RentHistory)
admin.site.register(Category)