from django.db import models

class Customer(models.Model):
    id=models.CharField(primary_key=True,max_length=250)
    name=models.CharField(max_length=700)
    email=models.EmailField()