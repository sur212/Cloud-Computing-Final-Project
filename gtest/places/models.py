from __future__ import unicode_literals
from django.db import models
#from django.core import urlresolvers


class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=200)

    def __str__(self):
        return self.user_name

class Guide(models.Model):
    guide_name = models.CharField(max_length=200)
    guide_number = models.CharField(max_length=15)
    guide_places = models.CharField(max_length=500)

    def __str__(self):
        return self.guide_name

class Country(models.Model):
    country_name = models.CharField(max_length=200)

    def __str__(self):
        return self.country_name



class City(models.Model):
    city_name = models.CharField(max_length=200)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name





