from django.db import models
from django.conf import settings


class Drone(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    type = models.CharField(max_length=20)
    image = models.URLField()

    manufacturer = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    basePrice = models.PositiveIntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    inStock = models.BooleanField(default=True)

    specs = models.JSONField(null=True, blank=True)
    discount = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    duration = models.IntegerField()
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.drone.name}"

    @property
    def drone_name(self):
        return self.drone.name

    @property
    def total_price(self):
        price_per_hour = self.drone.price
        return price_per_hour * self.duration

    @property
    def formatted_date(self):
        return self.start_date.strftime("%d.%m.%Y")

    @property
    def formatted_time(self):
        return self.start_date.strftime("%H:%M")



class DroneRating(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField()  # от 1 до 5

    class Meta:
        unique_together = ('drone', 'user')
