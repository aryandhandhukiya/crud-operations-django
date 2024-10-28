from django.db import models

class Persons(models.Model):
    fname=models.CharField(max_length=10)
    lname=models.CharField(max_length=10)
    age=models.IntegerField()
    email=models.EmailField(max_length=20)
    city=models.CharField(max_length=10)

