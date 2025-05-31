from django.db.models import Avg
from .models import Drone, DroneRating

def update_drone_rating(drone_id):
    avg = DroneRating.objects.filter(drone_id=drone_id).aggregate(Avg('score'))['score__avg']
    Drone.objects.filter(id=drone_id).update(rating=avg)
