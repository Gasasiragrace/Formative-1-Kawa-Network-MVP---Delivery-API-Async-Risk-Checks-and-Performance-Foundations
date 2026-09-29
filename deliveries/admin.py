from django.contrib import admin

from .models import Delivery, Farmer, Plot, PriceSchedule

admin.site.register(Farmer)
admin.site.register(Plot)
admin.site.register(Delivery)
admin.site.register(PriceSchedule)