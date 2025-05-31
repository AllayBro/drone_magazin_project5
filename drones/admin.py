
from django.contrib import admin
from .models import Drone, Booking  # Импортируем только модели дронов

admin.site.register(Drone)
admin.site.register(Booking)

