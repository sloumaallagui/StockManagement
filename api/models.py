from django.db import models

# Create your models here.

class Group(models.Model):
    name = models.TextField(default="")

class Product(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    ref = models.CharField(max_length=200)
    quantity = models.FloatField(default=0)

class Primary(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    stock1 = models.FloatField(default=0)
    stock2 = models.FloatField(default=0)
    stock3 = models.FloatField(default=0)

class Base(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)


