from django.db import models

# Create your models here.
class BookList(models.Model):
    title = models.CharField(max_length=150)
    author = models.CharField(max_length=150)
    price = models.IntegerField()

