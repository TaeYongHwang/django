from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=32)
    quantity = models.IntegerField()


class Product(models.Model):
    id = models.IntegerField(primary_key=True)
    imageId = models.CharField(max_length=100)
    name = models.TextField()
    price = models.IntegerField()
    gender = models.CharField(max_length=8)
    category = models.CharField(max_length=20)
    ingredients = models.TextField()
    monthlySales = models.IntegerField()


class Ingredient(models.Model):
    name = models.TextField()
    oily = models.CharField(max_length=1)
    dry = models.CharField(max_length=1)
    sensitive = models.CharField(max_length=1)

    @staticmethod
    def get_effect(ingredient, type):
        if type == "oily":
            return ingredient.oily
        elif type == "dry":
            return ingredient.dry
        else:
            return ingredient.sensitive

