from django.db import models
from django.contrib.auth.models import User

class StockDetails(models.Model):
    stock = models.CharField(max_length = 300, unique = True)
    user = models.ManyToManyField(User)
    
    def __str__(self):
        return f"{self.user}:{self.stock}"
