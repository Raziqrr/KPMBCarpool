from django.contrib import admin
from .models import Routes, Vehicle, Passenger, RideRequest, Driver

# Register your models here.

admin.site.register(Passenger)
admin.site.register(Driver)
admin.site.register(Routes)
admin.site.register(Vehicle)
admin.site.register(RideRequest)