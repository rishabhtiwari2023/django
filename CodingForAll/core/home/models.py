from django.db import models
class Car(models.Model):
    car_name=models.CharField(max_length=500)
    speed=models.IntegerField(default=50)
    def __str__(self)->str:
        return str(self.speed)+self.car_name
