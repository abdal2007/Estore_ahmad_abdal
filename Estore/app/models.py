from django.db import models

# Create your models here.
class Product(models.Model):
    title=models.CharField(max_length=200)
    price=models.IntegerField()
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title