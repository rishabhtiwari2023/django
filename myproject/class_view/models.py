from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Item(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)

	def __str__(self):
		return self.name