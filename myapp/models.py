# Create your models here.

from django.db import models

class EquityRecord(models.Model):
    code = models.CharField(max_length=10, unique=True) 
    name = models.CharField(max_length=100)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()  
    date = models.DateField()         

    def __str__(self):
        return self.name
