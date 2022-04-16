from django.db import models

# Create your models here.


class Book(models.Model):
    username = models.CharField(max_length=8)


class User(models.Model):
    username = models.CharField(max_length=8)
